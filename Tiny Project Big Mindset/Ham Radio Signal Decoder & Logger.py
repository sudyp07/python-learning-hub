#!/usr/bin/env python3
"""
Ham Radio Signal Decoder & Logger - Single File Project
Features:
- Decode WSJT-X UDP packets (FT8, FT4, JT65, etc.)
- Parse and log QSO data
- Export to ADIF format
- Display real-time decoded signals
- Band and frequency detection
- Grid square lookup
- Export to CSV/JSON
"""

import os
import sys
import json
import socket
import struct
import sqlite3
import threading
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from pathlib import Path
import hashlib

try:
    import tkinter as tk
    from tkinter import ttk, scrolledtext
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False
    print("⚠️  Tkinter not available. CLI mode only.")

# ============== CONSTANTS ==============

WSJT_PORT = 2237
WSJT_MULTICAST_GROUP = "224.0.0.1"
MAGIC_NUMBER = 0xADBCCBDA
MESSAGE_TYPES = {
    0: "Heartbeat",
    1: "Status",
    2: "Decoded",
    3: "WSPR",
    4: "Logged",
    5: "Close"
}

BANDS = {
    "160m": (1.8, 2.0),
    "80m": (3.5, 4.0),
    "60m": (5.3, 5.4),
    "40m": (7.0, 7.3),
    "30m": (10.1, 10.15),
    "20m": (14.0, 14.35),
    "17m": (18.068, 18.168),
    "15m": (21.0, 21.45),
    "12m": (24.89, 24.99),
    "10m": (28.0, 29.7),
    "6m": (50.0, 54.0),
    "2m": (144.0, 148.0),
    "70cm": (420.0, 450.0),
}

# ============== ADIF CONSTANTS ==============

ADIF_HEADER = """<ADIF_VER:5>3.1.4
<PROGRAMID:6>HamLog
<PROGRAMVERSION:4>1.0
<EOH>
"""

# ============== DATA CLASSES ==============

@dataclass
class DecodedSignal:
    """Represents a decoded signal from WSJT-X"""
    timestamp: datetime
    frequency: float
    mode: str
    message: str
    snr: int
    dt: float
    call: str = ""
    grid: str = ""
    report: str = ""
    is_cq: bool = False
    is_my_call: bool = False
    raw_data: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            'timestamp': self.timestamp.isoformat(),
            'frequency': self.frequency,
            'mode': self.mode,
            'message': self.message,
            'snr': self.snr,
            'dt': self.dt,
            'call': self.call,
            'grid': self.grid,
            'report': self.report,
            'is_cq': self.is_cq,
            'is_my_call': self.is_my_call
        }
    
    def get_band(self) -> str:
        """Determine band from frequency"""
        freq_mhz = self.frequency / 1_000_000
        for band, (low, high) in BANDS.items():
            if low <= freq_mhz <= high:
                return band
        return "Unknown"

    def get_preview(self, length: int = 50) -> str:
        """Get short preview"""
        if len(self.message) > length:
            return self.message[:length] + "..."
        return self.message


@dataclass
class QSO:
    """Represents a logged QSO"""
    callsign: str
    date: str  # YYYYMMDD
    time: str  # HHMM
    frequency: float
    mode: str
    rst_sent: str
    rst_rcvd: str
    grid: str
    name: str = ""
    qth: str = ""
    note: str = ""
    band: str = ""
    
    def to_adif(self) -> str:
        """Convert to ADIF format"""
        fields = [
            f"<CALL:{len(self.callsign)}>{self.callsign}",
            f"<QSO_DATE:{len(self.date)}>{self.date}",
            f"<TIME_ON:{len(self.time)}>{self.time}",
            f"<FREQ:{len(str(self.frequency))}>{self.frequency}",
            f"<BAND:{len(self.band)}>{self.band}",
            f"<MODE:{len(self.mode)}>{self.mode}",
            f"<RST_SENT:{len(self.rst_sent)}>{self.rst_sent}",
            f"<RST_RCVD:{len(self.rst_rcvd)}>{self.rst_rcvd}",
            f"<GRIDSQUARE:{len(self.grid)}>{self.grid}",
        ]
        if self.name:
            fields.append(f"<NAME:{len(self.name)}>{self.name}")
        if self.qth:
            fields.append(f"<QTH:{len(self.qth)}>{self.qth}")
        if self.note:
            fields.append(f"<COMMENT:{len(self.note)}>{self.note}")
        return " ".join(fields) + "\n"
    
    def to_dict(self) -> Dict:
        return {
            'callsign': self.callsign,
            'date': self.date,
            'time': self.time,
            'frequency': self.frequency,
            'mode': self.mode,
            'rst_sent': self.rst_sent,
            'rst_rcvd': self.rst_rcvd,
            'grid': self.grid,
            'name': self.name,
            'qth': self.qth,
            'note': self.note,
            'band': self.band
        }

# ============== WSJT-X DECODER ==============

class WSJTXDecoder:
    """Decode UDP packets from WSJT-X"""
    
    def __init__(self, my_callsign: str = ""):
        self.my_callsign = my_callsign.upper()
        self.signals: List[DecodedSignal] = []
        self.listeners = []
        self.running = False
        self.sock = None
    
    def start_listening(self, port: int = WSJT_PORT):
        """Start listening for UDP packets"""
        self.running = True
        
        try:
            # Create socket
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind(('', port))
            
            # Join multicast group if using multicast
            try:
                mreq = struct.pack("4sl", socket.inet_aton(WSJT_MULTICAST_GROUP), socket.INADDR_ANY)
                self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
            except:
                pass  # Not multicast
            
            self.sock.settimeout(1.0)
            
            while self.running:
                try:
                    data, addr = self.sock.recvfrom(4096)
                    self._process_packet(data)
                except socket.timeout:
                    continue
                except Exception as e:
                    print(f"⚠️  Socket error: {e}")
                    
        except Exception as e:
            print(f"❌ Failed to start listener: {e}")
        finally:
            if self.sock:
                self.sock.close()
    
    def stop_listening(self):
        """Stop listening"""
        self.running = False
        if self.sock:
            self.sock.close()
    
    def _process_packet(self, data: bytes):
        """Process a UDP packet from WSJT-X"""
        try:
            # Check magic number (first 4 bytes)
            if len(data) < 4:
                return
            
            magic = struct.unpack('>I', data[:4])[0]
            if magic != MAGIC_NUMBER:
                return
            
            # Parse packet type
            packet_type = data[4]
            
            # Parse based on type
            if packet_type == 2:  # Decoded
                self._parse_decoded_packet(data)
            elif packet_type == 4:  # Logged
                self._parse_logged_packet(data)
                
        except Exception as e:
            print(f"⚠️  Packet processing error: {e}")
    
    def _parse_decoded_packet(self, data: bytes):
        """Parse a decoded packet"""
        try:
            # Extract fields (based on WSJT-X UDP protocol)
            # Schema: See WSJT-X source for exact format
            offset = 8  # Skip header
            
            # Timestamp
            timestamp = datetime.now()
            
            # Frequency (8 bytes, double)
            if len(data) > offset + 8:
                freq = struct.unpack('>d', data[offset:offset+8])[0]
                offset += 8
            else:
                freq = 0.0
            
            # SNR (4 bytes, int)
            if len(data) > offset + 4:
                snr = struct.unpack('>i', data[offset:offset+4])[0]
                offset += 4
            else:
                snr = 0
            
            # DT (4 bytes, float)
            if len(data) > offset + 4:
                dt = struct.unpack('>f', data[offset:offset+4])[0]
                offset += 4
            else:
                dt = 0.0
            
            # Mode (20 bytes, string)
            if len(data) > offset + 20:
                mode = data[offset:offset+20].decode('utf-8', errors='ignore').strip('\x00')
                offset += 20
            else:
                mode = "Unknown"
            
            # Message (max 200 bytes, string)
            if len(data) > offset:
                message = data[offset:offset+200].decode('utf-8', errors='ignore').strip('\x00')
            else:
                message = ""
            
            # Parse message for details
            call = ""
            grid = ""
            report = ""
            is_cq = False
            is_my_call = False
            
            # Check for CQ
            if message.startswith("CQ "):
                is_cq = True
                parts = message.split()
                if len(parts) >= 2:
                    call = parts[1]
                    if len(parts) >= 3:
                        grid = parts[2]
            elif self.my_callsign and self.my_callsign in message:
                is_my_call = True
                # Try to extract grid
                import re
                grid_match = re.search(r'[A-Z]{2}\d{2}', message)
                if grid_match:
                    grid = grid_match.group()
                # Try to extract report (e.g., -15)
                report_match = re.search(r'[-+]?\d+', message)
                if report_match:
                    report = report_match.group()
            
            signal = DecodedSignal(
                timestamp=timestamp,
                frequency=freq,
                mode=mode,
                message=message,
                snr=snr,
                dt=dt,
                call=call,
                grid=grid,
                report=report,
                is_cq=is_cq,
                is_my_call=is_my_call,
                raw_data={'packet_type': 2}
            )
            
            self.signals.append(signal)
            
            # Notify listeners
            for listener in self.listeners:
                try:
                    listener(signal)
                except:
                    pass
                    
        except Exception as e:
            print(f"⚠️  Failed to parse decoded packet: {e}")
    
    def _parse_logged_packet(self, data: bytes):
        """Parse a logged QSO packet"""
        try:
            # Extract callsign (max 30 chars)
            offset = 8
            if len(data) > offset + 30:
                callsign = data[offset:offset+30].decode('utf-8', errors='ignore').strip('\x00')
                offset += 30
            else:
                callsign = "Unknown"
            
            # Extract grid (max 10 chars)
            if len(data) > offset + 10:
                grid = data[offset:offset+10].decode('utf-8', errors='ignore').strip('\x00')
                offset += 10
            else:
                grid = ""
            
            # Extract mode (max 10 chars)
            if len(data) > offset + 10:
                mode = data[offset:offset+10].decode('utf-8', errors='ignore').strip('\x00')
                offset += 10
            else:
                mode = "Unknown"
            
            print(f"✅ QSO Logged: {callsign} {grid} {mode}")
            
        except Exception as e:
            print(f"⚠️  Failed to parse logged packet: {e}")
    
    def add_listener(self, callback):
        """Add a callback for decoded signals"""
        self.listeners.append(callback)
    
    def get_recent(self, count: int = 20) -> List[DecodedSignal]:
        """Get most recent decoded signals"""
        return self.signals[-count:]

# ============== LOGGER ==============

class HamLogger:
    """Log QSOs and manage database"""
    
    def __init__(self, db_path: str = "ham_log.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # QSOs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS qsos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                callsign TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                frequency REAL,
                band TEXT,
                mode TEXT,
                rst_sent TEXT,
                rst_rcvd TEXT,
                grid TEXT,
                name TEXT,
                qth TEXT,
                note TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Decoded signals table (for historical tracking)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP NOT NULL,
                frequency REAL,
                mode TEXT,
                message TEXT,
                snr INTEGER,
                call TEXT,
                grid TEXT,
                band TEXT,
                is_cq BOOLEAN,
                is_my_call BOOLEAN
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def log_qso(self, qso: QSO) -> int:
        """Log a QSO"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO qsos 
            (callsign, date, time, frequency, band, mode, rst_sent, rst_rcvd, grid, name, qth, note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            qso.callsign, qso.date, qso.time, qso.frequency, qso.band,
            qso.mode, qso.rst_sent, qso.rst_rcvd, qso.grid,
            qso.name, qso.qth, qso.note
        ))
        
        qso_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return qso_id
    
    def save_signal(self, signal: DecodedSignal):
        """Save a decoded signal to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO signals 
            (timestamp, frequency, mode, message, snr, call, grid, band, is_cq, is_my_call)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            signal.timestamp.isoformat(),
            signal.frequency,
            signal.mode,
            signal.message,
            signal.snr,
            signal.call,
            signal.grid,
            signal.get_band(),
            signal.is_cq,
            signal.is_my_call
        ))
        
        conn.commit()
        conn.close()
    
    def get_qsos(self, limit: int = 100) -> List[Dict]:
        """Get recent QSOs"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM qsos
            ORDER BY created_at DESC
            LIMIT ?
        ''', (limit,))
        
        qsos = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return qsos
    
    def search_callsign(self, callsign: str) -> List[Dict]:
        """Search for a callsign"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM qsos
            WHERE callsign LIKE ?
            ORDER BY created_at DESC
        ''', (f'%{callsign}%',))
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results
    
    def export_adif(self, filename: str = None) -> str:
        """Export all QSOs to ADIF format"""
        if not filename:
            filename = f"ham_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.adi"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM qsos ORDER BY created_at ASC')
        qsos = cursor.fetchall()
        conn.close()
        
        with open(filename, 'w') as f:
            f.write(ADIF_HEADER)
            for row in qsos:
                # Reconstruct QSO object
                qso = QSO(
                    callsign=row[1],
                    date=row[2],
                    time=row[3],
                    frequency=row[4],
                    band=row[5] or "",
                    mode=row[6] or "",
                    rst_sent=row[7] or "",
                    rst_rcvd=row[8] or "",
                    grid=row[9] or "",
                    name=row[10] or "",
                    qth=row[11] or "",
                    note=row[12] or ""
                )
                f.write(qso.to_adif())
        
        return filename
    
    def export_json(self, filename: str = None) -> str:
        """Export QSOs to JSON"""
        if not filename:
            filename = f"ham_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        qsos = self.get_qsos(limit=10000)
        
        with open(filename, 'w') as f:
            json.dump(qsos, f, indent=2)
        
        return filename
    
    def get_stats(self) -> Dict:
        """Get logging statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total QSOs
        cursor.execute('SELECT COUNT(*) FROM qsos')
        total_qsos = cursor.fetchone()[0]
        
        # Unique callsigns
        cursor.execute('SELECT COUNT(DISTINCT callsign) FROM qsos')
        unique_calls = cursor.fetchone()[0]
        
        # By band
        cursor.execute('''
            SELECT band, COUNT(*) FROM qsos
            WHERE band IS NOT NULL AND band != ''
            GROUP BY band
            ORDER BY COUNT(*) DESC
        ''')
        by_band = cursor.fetchall()
        
        # By mode
        cursor.execute('''
            SELECT mode, COUNT(*) FROM qsos
            WHERE mode IS NOT NULL AND mode != ''
            GROUP BY mode
            ORDER BY COUNT(*) DESC
        ''')
        by_mode = cursor.fetchall()
        
        conn.close()
        
        return {
            'total_qsos': total_qsos,
            'unique_callsigns': unique_calls,
            'by_band': by_band,
            'by_mode': by_mode
        }

# ============== CLI INTERFACE ==============

class HamRadioCLI:
    """Command line interface"""
    
    def __init__(self):
        self.decoder = None
        self.logger = HamLogger()
        self.my_callsign = ""
        self.running = False
    
    def run(self):
        """Run the CLI"""
        self.show_welcome()
        
        # Setup callsign
        callsign = input("\nEnter your callsign (optional): ").strip().upper()
        if callsign:
            self.my_callsign = callsign
        
        while True:
            try:
                command = input("\n📡 > ").strip()
                
                if not command:
                    continue
                
                parts = command.split()
                cmd = parts[0].lower()
                
                if cmd in ['quit', 'exit', 'q']:
                    self.stop_decoder()
                    print("👋 73!")
                    break
                elif cmd == 'help':
                    self.show_help()
                elif cmd == 'listen':
                    self.start_decoder()
                elif cmd == 'stop':
                    self.stop_decoder()
                elif cmd == 'list':
                    self.list_signals()
                elif cmd == 'log':
                    self.log_qso_interactive()
                elif cmd == 'qsos':
                    self.show_qsos()
                elif cmd == 'export':
                    self.export_logs()
                elif cmd == 'stats':
                    self.show_stats()
                elif cmd == 'search':
                    self.search_callsign(parts[1] if len(parts) > 1 else '')
                else:
                    print(f"❌ Unknown command: {cmd}")
                    print("   Type 'help' for available commands")
                    
            except KeyboardInterrupt:
                print("\n👋 73!")
                self.stop_decoder()
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def show_welcome(self):
        """Show welcome message"""
        print("\n" + "="*60)
        print("📡 HAM RADIO SIGNAL DECODER & LOGGER")
        print("="*60)
        print("\n🔍 Decodes WSJT-X UDP packets (FT8, FT4, JT65, etc.)")
        print("📝 Logs QSOs with full details")
        print("📤 Exports to ADIF, JSON, CSV")
        print("\nType 'help' to see all commands")
        print("="*60)
    
    def show_help(self):
        """Show help message"""
        print("\n" + "="*60)
        print("📡 Available Commands:")
        print("="*60)
        print("\n  📡 listen        - Start listening for decoded signals")
        print("  ⏹️ stop          - Stop listening")
        print("  📋 list          - Show recent decoded signals")
        print("  ✏️ log           - Log a QSO manually")
        print("  📚 qsos          - Show logged QSOs")
        print("  📤 export        - Export logs to ADIF/JSON")
        print("  📊 stats         - Show logging statistics")
        print("  🔍 search <call> - Search for a callsign")
        print("  ❓ help          - Show this help")
        print("  🚪 quit          - Exit")
        print("\n" + "="*60)
    
    def start_decoder(self):
        """Start the decoder"""
        if self.decoder and self.running:
            print("⚠️  Already listening")
            return
        
        self.decoder = WSJTXDecoder(self.my_callsign)
        self.decoder.add_listener(self._on_signal)
        self.running = True
        
        print(f"📡 Listening for WSJT-X packets on port {WSJT_PORT}...")
        
        # Start in background thread
        thread = threading.Thread(target=self.decoder.start_listening, daemon=True)
        thread.start()
        
        print("✅ Listening started")
    
    def stop_decoder(self):
        """Stop the decoder"""
        if self.decoder:
            self.decoder.stop_listening()
            self.running = False
            print("⏹️ Listening stopped")
    
    def _on_signal(self, signal: DecodedSignal):
        """Callback for decoded signals"""
        # Print to console
        band = signal.get_band()
        print(f"\n📢 {signal.timestamp.strftime('%H:%M:%S')} [{band}] {signal.mode}")
        print(f"   {signal.message} (SNR: {signal.snr}dB, DT: {signal.dt:.2f}s)")
        if signal.is_cq:
            print(f"   🔍 CQ from {signal.call} @ {signal.grid}")
        
        # Save to database
        self.logger.save_signal(signal)
    
    def list_signals(self):
        """List recent signals"""
        if not self.decoder:
            print("❌ Not listening. Use 'listen' first")
            return
        
        signals = self.decoder.get_recent(20)
        if not signals:
            print("📭 No signals decoded yet")
            return
        
        print(f"\n📋 Recent Signals ({len(signals)})")
        print("-"*70)
        
        for signal in reversed(signals):
            band = signal.get_band()
            cq_marker = "🔍 " if signal.is_cq else "   "
            print(f"  {cq_marker} {signal.timestamp.strftime('%H:%M:%S')} "
                  f"[{band:>6}] {signal.mode:>6} "
                  f"SNR:{signal.snr:>3}dB {signal.message[:40]}")
    
    def log_qso_interactive(self):
        """Log a QSO interactively"""
        print("\n✏️ Log QSO")
        print("-"*40)
        
        callsign = input("Callsign: ").strip().upper()
        if not callsign:
            print("❌ Callsign required")
            return
        
        date_str = input("Date (YYYYMMDD, press enter for today): ").strip()
        if not date_str:
            date_str = datetime.now().strftime("%Y%m%d")
        
        time_str = input("Time (HHMM, press enter for now): ").strip()
        if not time_str:
            time_str = datetime.now().strftime("%H%M")
        
        freq_str = input("Frequency (MHz): ").strip()
        frequency = float(freq_str) * 1_000_000 if freq_str else 0.0
        
        band = input("Band (e.g., 20m, 40m): ").strip()
        if not band:
            # Try to detect from frequency
            if frequency > 0:
                for b, (low, high) in BANDS.items():
                    freq_mhz = frequency / 1_000_000
                    if low <= freq_mhz <= high:
                        band = b
                        break
            if not band:
                band = "Unknown"
        
        mode = input("Mode: ").strip().upper() or "FT8"
        rst_sent = input("RST Sent: ").strip() or "59"
        rst_rcvd = input("RST Received: ").strip() or "59"
        grid = input("Grid Square: ").strip().upper()
        name = input("Name: ").strip()
        qth = input("QTH: ").strip()
        note = input("Note: ").strip()
        
        qso = QSO(
            callsign=callsign,
            date=date_str,
            time=time_str,
            frequency=frequency,
            mode=mode,
            rst_sent=rst_sent,
            rst_rcvd=rst_rcvd,
            grid=grid,
            name=name,
            qth=qth,
            note=note,
            band=band
        )
        
        self.logger.log_qso(qso)
        print(f"✅ QSO with {callsign} logged!")
    
    def show_qsos(self):
        """Show logged QSOs"""
        qsos = self.logger.get_qsos(20)
        if not qsos:
            print("📭 No QSOs logged")
            return
        
        print(f"\n📚 Recent QSOs ({len(qsos)})")
        print("-"*80)
        print(f"{'#':>3} {'Callsign':<10} {'Date':<10} {'Time':<6} {'Band':<8} {'Mode':<6} {'Grid':<6}")
        print("-"*80)
        
        for i, qso in enumerate(qsos, 1):
            print(f"{i:>3} {qso['callsign']:<10} {qso['date']:<10} "
                  f"{qso['time']:<6} {qso['band']:<8} {qso['mode']:<6} {qso['grid']:<6}")
    
    def export_logs(self):
        """Export logs"""
        print("\n📤 Export Options:")
        print("  1. ADIF")
        print("  2. JSON")
        print("  3. CSV (compatible with spreadsheet apps)")
        
        choice = input("Choose option (1-3): ").strip()
        
        if choice == '1':
            filename = self.logger.export_adif()
            print(f"✅ Exported to {filename}")
        elif choice == '2':
            filename = self.logger.export_json()
            print(f"✅ Exported to {filename}")
        elif choice == '3':
            self.export_csv()
        else:
            print("❌ Invalid choice")
    
    def export_csv(self):
        """Export to CSV"""
        filename = f"ham_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        qsos = self.logger.get_qsos(limit=10000)
        
        import csv
        with open(filename, 'w', newline='') as f:
            if qsos:
                writer = csv.DictWriter(f, fieldnames=qsos[0].keys())
                writer.writeheader()
                writer.writerows(qsos)
        
        print(f"✅ Exported to {filename}")
    
    def show_stats(self):
        """Show statistics"""
        stats = self.logger.get_stats()
        
        print("\n📊 Logging Statistics")
        print("-"*40)
        print(f"  📝 Total QSOs:       {stats['total_qsos']}")
        print(f"  👥 Unique Callsigns: {stats['unique_callsigns']}")
        
        if stats['by_band']:
            print("\n  📡 By Band:")
            for band, count in stats['by_band'][:5]:
                print(f"     • {band}: {count}")
        
        if stats['by_mode']:
            print("\n  📡 By Mode:")
            for mode, count in stats['by_mode'][:5]:
                print(f"     • {mode}: {count}")
    
    def search_callsign(self, callsign: str):
        """Search for a callsign"""
        if not callsign:
            print("❌ Please provide a callsign: search <callsign>")
            return
        
        results = self.logger.search_callsign(callsign)
        if not results:
            print(f"🔍 No QSOs found for {callsign}")
            return
        
        print(f"\n🔍 Found {len(results)} QSOs for {callsign}")
        print("-"*70)
        for qso in results[:10]:
            print(f"  {qso['date']} {qso['time']} "
                  f"[{qso['band']}] {qso['mode']} "
                  f"RST: {qso['rst_sent']}/{qso['rst_rcvd']}")
            if qso['grid']:
                print(f"     Grid: {qso['grid']}")

# ============== MAIN ==============

def main():
    """Main entry point"""
    # Check for GUI mode
    if len(sys.argv) > 1 and sys.argv[1] == '--gui' and GUI_AVAILABLE:
        print("GUI mode coming soon!")
        return
    
    # CLI mode
    cli = HamRadioCLI()
    cli.run()

if __name__ == "__main__":
    main()