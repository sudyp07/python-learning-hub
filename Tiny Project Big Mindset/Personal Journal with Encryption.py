#!/usr/bin/env python3
"""
Personal Journal with Encryption - Single File Project
Features:
- Write daily entries with timestamps
- Encrypt/decrypt with password (Fernet)
- Search by date or keyword
- Export to PDF
"""

import os
import sys
import json
import base64
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import getpass

# Encryption libraries
try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
except ImportError:
    print("❌ cryptography not installed. Run: pip install cryptography")
    sys.exit(1)

# PDF export libraries
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.enums import TA_LEFT, TA_CENTER
except ImportError:
    print("⚠️  reportlab not installed. PDF export will be disabled.")
    print("   Install with: pip install reportlab")
    PDF_AVAILABLE = False
else:
    PDF_AVAILABLE = True

# ============== CONSTANTS ==============

JOURNAL_FILE = "journal.enc"
KEY_FILE = "journal.key"
BACKUP_DIR = "journal_backups"
DEFAULT_DATE_FORMAT = "%Y-%m-%d"
DEFAULT_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# ============== ENCRYPTION ==============

class JournalEncryption:
    """Handle encryption/decryption of journal entries"""
    
    def __init__(self, password: str):
        self.password = password
        self.salt = b'journal_salt_2024'  # Fixed salt for consistency
        self.key = self._derive_key(password)
        self.cipher = Fernet(self.key)
    
    def _derive_key(self, password: str) -> bytes:
        """Derive encryption key from password"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def encrypt(self, data: str) -> bytes:
        """Encrypt string data"""
        return self.cipher.encrypt(data.encode())
    
    def decrypt(self, encrypted_data: bytes) -> str:
        """Decrypt encrypted data"""
        return self.cipher.decrypt(encrypted_data).decode()
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Create a hash of the password for verification"""
        return hashlib.sha256(password.encode()).hexdigest()

# ============== JOURNAL ENTRY ==============

class JournalEntry:
    """Represents a single journal entry"""
    
    def __init__(self, content: str, timestamp: Optional[datetime] = None, 
                 entry_id: Optional[str] = None):
        self.content = content
        self.timestamp = timestamp or datetime.now()
        self.entry_id = entry_id or self.timestamp.strftime("%Y%m%d%H%M%S")
    
    def to_dict(self) -> Dict:
        """Convert entry to dictionary for JSON serialization"""
        return {
            'id': self.entry_id,
            'timestamp': self.timestamp.isoformat(),
            'content': self.content
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'JournalEntry':
        """Create entry from dictionary"""
        timestamp = datetime.fromisoformat(data['timestamp'])
        return cls(
            content=data['content'],
            timestamp=timestamp,
            entry_id=data['id']
        )
    
    def get_date_str(self) -> str:
        """Get date as string"""
        return self.timestamp.strftime(DEFAULT_DATE_FORMAT)
    
    def get_datetime_str(self) -> str:
        """Get datetime as string"""
        return self.timestamp.strftime(DEFAULT_DATETIME_FORMAT)
    
    def get_preview(self, length: int = 50) -> str:
        """Get short preview of content"""
        preview = self.content.replace('\n', ' ')
        if len(preview) > length:
            return preview[:length] + "..."
        return preview

# ============== JOURNAL MANAGER ==============

class JournalManager:
    """Main journal management class"""
    
    def __init__(self, password: str):
        self.password = password
        self.encryption = JournalEncryption(password)
        self.entries: List[JournalEntry] = []
        self.load_journal()
    
    def load_journal(self):
        """Load journal from encrypted file"""
        if not os.path.exists(JOURNAL_FILE):
            return
        
        try:
            with open(JOURNAL_FILE, 'rb') as f:
                encrypted_data = f.read()
            
            if not encrypted_data:
                return
            
            # Decrypt and parse JSON
            json_data = self.encryption.decrypt(encrypted_data)
            data = json.loads(json_data)
            
            # Convert to JournalEntry objects
            self.entries = [JournalEntry.from_dict(entry_data) for entry_data in data]
            print(f"📖 Loaded {len(self.entries)} entries")
            
        except Exception as e:
            print(f"❌ Failed to load journal: {e}")
            print("   Password might be incorrect or file corrupted.")
            self.entries = []
    
    def save_journal(self):
        """Save journal to encrypted file"""
        try:
            # Convert entries to dict
            data = [entry.to_dict() for entry in self.entries]
            json_data = json.dumps(data, indent=2)
            
            # Encrypt and save
            encrypted_data = self.encryption.encrypt(json_data)
            
            # Create backup before saving
            self._create_backup()
            
            with open(JOURNAL_FILE, 'wb') as f:
                f.write(encrypted_data)
            
            print(f"💾 Journal saved ({len(self.entries)} entries)")
            
        except Exception as e:
            print(f"❌ Failed to save journal: {e}")
    
    def _create_backup(self):
        """Create a backup of the journal"""
        if not os.path.exists(JOURNAL_FILE):
            return
        
        os.makedirs(BACKUP_DIR, exist_ok=True)
        backup_file = os.path.join(
            BACKUP_DIR, 
            f"journal_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.enc"
        )
        
        try:
            with open(JOURNAL_FILE, 'rb') as src:
                with open(backup_file, 'wb') as dst:
                    dst.write(src.read())
        except:
            pass
    
    def add_entry(self, content: str) -> JournalEntry:
        """Add a new journal entry"""
        entry = JournalEntry(content)
        self.entries.append(entry)
        self.save_journal()
        return entry
    
    def get_entries_by_date(self, date_str: str) -> List[JournalEntry]:
        """Get entries for a specific date"""
        target_date = datetime.strptime(date_str, DEFAULT_DATE_FORMAT).date()
        return [
            entry for entry in self.entries
            if entry.timestamp.date() == target_date
        ]
    
    def get_entries_by_date_range(self, start_date: str, end_date: str) -> List[JournalEntry]:
        """Get entries within a date range"""
        start = datetime.strptime(start_date, DEFAULT_DATE_FORMAT)
        end = datetime.strptime(end_date, DEFAULT_DATE_FORMAT)
        return [
            entry for entry in self.entries
            if start <= entry.timestamp <= end
        ]
    
    def search_entries(self, keyword: str, case_sensitive: bool = False) -> List[JournalEntry]:
        """Search entries by keyword"""
        if not case_sensitive:
            keyword = keyword.lower()
            return [
                entry for entry in self.entries
                if keyword in entry.content.lower()
            ]
        else:
            return [
                entry for entry in self.entries
                if keyword in entry.content
            ]
    
    def get_today_entries(self) -> List[JournalEntry]:
        """Get today's entries"""
        today = datetime.now().date()
        return [
            entry for entry in self.entries
            if entry.timestamp.date() == today
        ]
    
    def get_recent_entries(self, count: int = 10) -> List[JournalEntry]:
        """Get most recent entries"""
        return sorted(self.entries, key=lambda x: x.timestamp, reverse=True)[:count]
    
    def get_entry_by_id(self, entry_id: str) -> Optional[JournalEntry]:
        """Get entry by ID"""
        for entry in self.entries:
            if entry.entry_id == entry_id:
                return entry
        return None
    
    def delete_entry(self, entry_id: str) -> bool:
        """Delete an entry by ID"""
        for i, entry in enumerate(self.entries):
            if entry.entry_id == entry_id:
                del self.entries[i]
                self.save_journal()
                return True
        return False
    
    def get_statistics(self) -> Dict:
        """Get journal statistics"""
        if not self.entries:
            return {
                'total_entries': 0,
                'first_entry': None,
                'last_entry': None,
                'days_with_entries': 0,
                'avg_entries_per_day': 0
            }
        
        dates = set(entry.timestamp.date() for entry in self.entries)
        days_with_entries = len(dates)
        total_days = (datetime.now() - min(entry.timestamp for entry in self.entries)).days + 1
        
        return {
            'total_entries': len(self.entries),
            'first_entry': min(entry.timestamp for entry in self.entries),
            'last_entry': max(entry.timestamp for entry in self.entries),
            'days_with_entries': days_with_entries,
            'avg_entries_per_day': len(self.entries) / max(1, total_days)
        }

# ============== PDF EXPORTER ==============

class JournalPDFExporter:
    """Export journal entries to PDF"""
    
    @staticmethod
    def export_to_pdf(entries: List[JournalEntry], filename: str = None):
        """Export entries to PDF"""
        if not PDF_AVAILABLE:
            print("❌ PDF export not available. Install reportlab.")
            return False
        
        if not entries:
            print("❌ No entries to export")
            return False
        
        if not filename:
            filename = f"journal_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        try:
            doc = SimpleDocTemplate(filename, pagesize=letter)
            styles = getSampleStyleSheet()
            
            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                alignment=TA_CENTER
            )
            
            entry_style = ParagraphStyle(
                'EntryStyle',
                parent=styles['Normal'],
                fontSize=11,
                spaceAfter=12,
                alignment=TA_LEFT
            )
            
            date_style = ParagraphStyle(
                'DateStyle',
                parent=styles['Normal'],
                fontSize=10,
                textColor='#666666',
                spaceAfter=6
            )
            
            story = []
            
            # Title
            story.append(Paragraph("📖 Personal Journal", title_style))
            story.append(Spacer(1, 0.2*inch))
            
            # Stats
            stats = f"Total entries: {len(entries)}"
            story.append(Paragraph(stats, styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
            
            # Entries
            for entry in sorted(entries, key=lambda x: x.timestamp):
                # Date
                date_str = entry.get_datetime_str()
                story.append(Paragraph(f"<b>{date_str}</b>", date_style))
                
                # Content
                content = entry.content.replace('\n', '<br/>')
                story.append(Paragraph(content, entry_style))
                
                # Separator
                story.append(Spacer(1, 0.1*inch))
                story.append(Paragraph("—" * 50, styles['Normal']))
                story.append(Spacer(1, 0.2*inch))
            
            # Build PDF
            doc.build(story)
            print(f"✅ PDF exported successfully: {filename}")
            return True
            
        except Exception as e:
            print(f"❌ PDF export failed: {e}")
            return False

# ============== CLI INTERFACE ==============

class JournalCLI:
    """Command-line interface for the journal"""
    
    def __init__(self):
        self.journal = None
        self.setup_journal()
    
    def setup_journal(self):
        """Setup or load journal with password"""
        print("\n" + "="*60)
        print("📖 PERSONAL JOURNAL WITH ENCRYPTION")
        print("="*60)
        
        # Check if journal exists
        if os.path.exists(JOURNAL_FILE):
            print("\n🔐 Existing journal found.")
            
            # Try up to 3 times for password
            for attempt in range(3):
                password = getpass.getpass("Enter password: ")
                try:
                    self.journal = JournalManager(password)
                    if self.journal.entries is not None:
                        print(f"✅ Loaded {len(self.journal.entries)} entries")
                        break
                except:
                    print(f"❌ Wrong password. Attempts left: {2-attempt}")
                    if attempt == 2:
                        print("❌ Too many failed attempts. Exiting.")
                        sys.exit(1)
        else:
            print("\n📝 Creating new journal...")
            password = getpass.getpass("Create password: ")
            confirm = getpass.getpass("Confirm password: ")
            
            if password != confirm:
                print("❌ Passwords do not match. Exiting.")
                sys.exit(1)
            
            self.journal = JournalManager(password)
            print("✅ New journal created!")
    
    def run(self):
        """Run the CLI"""
        self.show_help()
        
        while True:
            try:
                command = input("\n📝 > ").strip()
                
                if not command:
                    continue
                
                parts = command.split()
                cmd = parts[0].lower()
                
                if cmd in ['quit', 'exit', 'q']:
                    self.journal.save_journal()
                    print("👋 Goodbye!")
                    break
                elif cmd == 'help':
                    self.show_help()
                elif cmd in ['add', 'a']:
                    self.add_entry()
                elif cmd in ['list', 'ls']:
                    self.list_entries(parts[1:] if len(parts) > 1 else [])
                elif cmd in ['today', 't']:
                    self.show_today()
                elif cmd in ['search', 's']:
                    self.search_entries(' '.join(parts[1:]) if len(parts) > 1 else '')
                elif cmd in ['date', 'd']:
                    self.show_by_date(parts[1] if len(parts) > 1 else '')
                elif cmd in ['range', 'r']:
                    self.show_date_range(parts[1] if len(parts) > 1 else '', 
                                        parts[2] if len(parts) > 2 else '')
                elif cmd in ['export', 'e']:
                    self.export_pdf(' '.join(parts[1:]) if len(parts) > 1 else None)
                elif cmd == 'stats':
                    self.show_stats()
                elif cmd in ['delete', 'del']:
                    self.delete_entry(parts[1] if len(parts) > 1 else '')
                elif cmd == 'clear':
                    self.clear_screen()
                else:
                    print(f"❌ Unknown command: {cmd}")
                    print("   Type 'help' for available commands")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                self.journal.save_journal()
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def show_help(self):
        """Show help message"""
        print("\n" + "="*60)
        print("📖 Available Commands:")
        print("="*60)
        print("\n  📝 add / a          - Add a new journal entry")
        print("  📋 list / ls [n]    - List entries (optional: number of entries)")
        print("  📅 today / t        - Show today's entries")
        print("  🔍 search <keyword> - Search entries by keyword")
        print("  📆 date <YYYY-MM-DD> - Show entries for specific date")
        print("  📊 range <start> <end> - Show entries in date range")
        print("  📤 export [filename] - Export to PDF")
        print("  📈 stats            - Show journal statistics")
        print("  🗑️  delete <id>     - Delete entry by ID")
        print("  🧹 clear            - Clear screen")
        print("  ❓ help             - Show this help")
        print("  🚪 quit / exit / q  - Save and exit")
        print("\n" + "="*60)
    
    def add_entry(self):
        """Add a new entry"""
        print("\n📝 Enter your journal entry (type 'END' on a new line to finish):")
        print("-" * 50)
        
        lines = []
        while True:
            line = input()
            if line.strip() == 'END':
                break
            lines.append(line)
        
        content = '\n'.join(lines).strip()
        if not content:
            print("❌ Empty entry. Cancelled.")
            return
        
        entry = self.journal.add_entry(content)
        print(f"✅ Entry added! (ID: {entry.entry_id})")
    
    def list_entries(self, args: List[str]):
        """List recent entries"""
        count = 10
        if args and args[0].isdigit():
            count = int(args[0])
        
        entries = self.journal.get_recent_entries(count)
        if not entries:
            print("📭 No entries found.")
            return
        
        print(f"\n📋 Recent {len(entries)} entries:")
        print("-" * 70)
        for entry in entries:
            preview = entry.get_preview(40)
            print(f"  [{entry.entry_id[:8]}] {entry.get_datetime_str()}")
            print(f"    {preview}")
            print()
    
    def show_today(self):
        """Show today's entries"""
        entries = self.journal.get_today_entries()
        if not entries:
            print("📭 No entries for today.")
            return
        
        print(f"\n📅 Today's entries ({datetime.now().strftime(DEFAULT_DATE_FORMAT)}):")
        print("-" * 70)
        for entry in entries:
            print(f"  [{entry.entry_id[:8]}] {entry.get_datetime_str()}")
            print(f"  {entry.content}")
            print()
    
    def search_entries(self, keyword: str):
        """Search entries by keyword"""
        if not keyword:
            print("❌ Please provide a keyword: search <keyword>")
            return
        
        entries = self.journal.search_entries(keyword)
        if not entries:
            print(f"🔍 No entries found containing '{keyword}'")
            return
        
        print(f"\n🔍 Found {len(entries)} entries containing '{keyword}':")
        print("-" * 70)
        for entry in entries:
            preview = entry.get_preview(50)
            print(f"  [{entry.entry_id[:8]}] {entry.get_datetime_str()}")
            print(f"    {preview}")
            print()
    
    def show_by_date(self, date_str: str):
        """Show entries for a specific date"""
        if not date_str:
            print("❌ Please provide a date: date <YYYY-MM-DD>")
            return
        
        try:
            entries = self.journal.get_entries_by_date(date_str)
            if not entries:
                print(f"📭 No entries for {date_str}")
                return
            
            print(f"\n📅 Entries for {date_str}:")
            print("-" * 70)
            for entry in entries:
                print(f"  [{entry.entry_id[:8]}] {entry.get_datetime_str()}")
                print(f"  {entry.content}")
                print()
        except ValueError:
            print("❌ Invalid date format. Use YYYY-MM-DD")
    
    def show_date_range(self, start_date: str, end_date: str):
        """Show entries in date range"""
        if not start_date or not end_date:
            print("❌ Please provide start and end dates: range <start> <end>")
            return
        
        try:
            entries = self.journal.get_entries_by_date_range(start_date, end_date)
            if not entries:
                print(f"📭 No entries from {start_date} to {end_date}")
                return
            
            print(f"\n📊 Entries from {start_date} to {end_date}:")
            print("-" * 70)
            for entry in entries:
                print(f"  [{entry.entry_id[:8]}] {entry.get_datetime_str()}")
                print(f"  {entry.get_preview(60)}")
                print()
        except ValueError:
            print("❌ Invalid date format. Use YYYY-MM-DD")
    
    def export_pdf(self, filename: Optional[str] = None):
        """Export to PDF"""
        if not self.journal.entries:
            print("❌ No entries to export")
            return
        
        # Ask for date range or all
        print("\n📤 Export options:")
        print("  1. All entries")
        print("  2. Last N days")
        print("  3. Date range")
        
        choice = input("Choose option (1-3): ").strip()
        
        entries_to_export = []
        
        if choice == '1':
            entries_to_export = self.journal.entries
        elif choice == '2':
            try:
                days = int(input("Number of days: "))
                cutoff = datetime.now() - timedelta(days=days)
                entries_to_export = [
                    e for e in self.journal.entries
                    if e.timestamp >= cutoff
                ]
            except:
                print("❌ Invalid input")
                return
        elif choice == '3':
            try:
                start = input("Start date (YYYY-MM-DD): ")
                end = input("End date (YYYY-MM-DD): ")
                entries_to_export = self.journal.get_entries_by_date_range(start, end)
            except:
                print("❌ Invalid date format")
                return
        else:
            print("❌ Invalid choice")
            return
        
        if not entries_to_export:
            print("❌ No entries match the criteria")
            return
        
        # Export
        if not filename:
            filename = f"journal_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        JournalPDFExporter.export_to_pdf(entries_to_export, filename)
    
    def show_stats(self):
        """Show journal statistics"""
        stats = self.journal.get_statistics()
        
        print("\n📈 Journal Statistics:")
        print("-" * 40)
        print(f"  📝 Total entries:      {stats['total_entries']}")
        print(f"  📅 Days with entries:  {stats['days_with_entries']}")
        print(f"  📊 Avg entries/day:    {stats['avg_entries_per_day']:.2f}")
        
        if stats['first_entry']:
            print(f"  🐣 First entry:        {stats['first_entry'].strftime(DEFAULT_DATETIME_FORMAT)}")
        if stats['last_entry']:
            print(f"  🦋 Last entry:         {stats['last_entry'].strftime(DEFAULT_DATETIME_FORMAT)}")
    
    def delete_entry(self, entry_id: str):
        """Delete an entry"""
        if not entry_id:
            print("❌ Please provide entry ID: delete <id>")
            return
        
        if self.journal.delete_entry(entry_id):
            print(f"✅ Entry {entry_id} deleted")
        else:
            print(f"❌ Entry {entry_id} not found")
    
    @staticmethod
    def clear_screen():
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

# ============== MAIN ==============

def main():
    """Main entry point"""
    # Check for command line arguments
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        print("""
Personal Journal with Encryption - Usage:

  python journal.py              - Interactive journal
  python journal.py --help       - Show this help
        """)
        return
    
    # Run the journal
    try:
        cli = JournalCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Fatal error: {e}")

if __name__ == "__main__":
    main()