#!/usr/bin/env python3
"""
Unit Converter - Single File Project
Features:
- Convert between length, weight, temperature, currency
- Batch conversion from CSV
- Interactive CLI with history
"""

import json
import csv
import os
import sys
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Union
import requests
from pathlib import Path

# ============== CONVERSION DATA ==============

CONVERSION_FACTORS = {
    "length": {
        "meter": 1.0,
        "kilometer": 1000.0,
        "centimeter": 0.01,
        "millimeter": 0.001,
        "mile": 1609.344,
        "yard": 0.9144,
        "foot": 0.3048,
        "inch": 0.0254,
        "nautical_mile": 1852.0
    },
    "weight": {
        "kilogram": 1.0,
        "gram": 0.001,
        "milligram": 0.000001,
        "metric_ton": 1000.0,
        "pound": 0.453592,
        "ounce": 0.0283495,
        "stone": 6.35029
    }
}

# Currency cache (to avoid API rate limits)
CURRENCY_CACHE = {}
CACHE_FILE = "currency_cache.json"

# ============== CURRENCY CONVERTER ==============

def get_exchange_rates(base_currency: str = "USD") -> Dict[str, float]:
    """Fetch live exchange rates with caching"""
    global CURRENCY_CACHE
    
    # Check cache first
    if base_currency in CURRENCY_CACHE:
        cache_time = CURRENCY_CACHE[base_currency].get("timestamp", 0)
        # Cache valid for 1 hour
        if datetime.now().timestamp() - cache_time < 3600:
            return CURRENCY_CACHE[base_currency]["rates"]
    
    try:
        # Using free API (no API key required)
        url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        rates = data.get("rates", {})
        # Add base currency itself
        rates[base_currency] = 1.0
        
        # Update cache
        CURRENCY_CACHE[base_currency] = {
            "rates": rates,
            "timestamp": datetime.now().timestamp()
        }
        
        # Save cache to file
        save_currency_cache()
        
        return rates
    except Exception as e:
        print(f"⚠️  Currency API error: {e}")
        # Return cached rates even if expired
        if base_currency in CURRENCY_CACHE:
            print("📦 Using cached rates...")
            return CURRENCY_CACHE[base_currency]["rates"]
        return {base_currency: 1.0}

def save_currency_cache():
    """Save currency cache to file"""
    try:
        with open(CACHE_FILE, "w") as f:
            json.dump(CURRENCY_CACHE, f)
    except:
        pass

def load_currency_cache():
    """Load currency cache from file"""
    global CURRENCY_CACHE
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r") as f:
                CURRENCY_CACHE = json.load(f)
    except:
        pass

def convert_currency(value: float, from_unit: str, to_unit: str) -> float:
    """Convert between currencies"""
    from_unit = from_unit.upper()
    to_unit = to_unit.upper()
    
    rates = get_exchange_rates(from_unit)
    if to_unit not in rates:
        raise ValueError(f"Unknown currency: {to_unit}")
    
    return value * rates[to_unit]

# ============== LENGTH/WEIGHT CONVERTER ==============

def convert_standard(value: float, from_unit: str, to_unit: str, category: str) -> float:
    """Convert length or weight units"""
    if category not in CONVERSION_FACTORS:
        raise ValueError(f"Unknown category: {category}")
    
    factors = CONVERSION_FACTORS[category]
    
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    
    if from_unit not in factors:
        raise ValueError(f"Unknown unit: {from_unit}")
    if to_unit not in factors:
        raise ValueError(f"Unknown unit: {to_unit}")
    
    # Convert to base unit (meter or kilogram), then to target
    base_value = value * factors[from_unit]
    return base_value / factors[to_unit]

# ============== TEMPERATURE CONVERTER ==============

def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """Convert temperature between Celsius, Fahrenheit, Kelvin"""
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    
    # First convert to Celsius
    if from_unit == "celsius" or from_unit == "c":
        celsius = value
    elif from_unit == "fahrenheit" or from_unit == "f":
        celsius = (value - 32) * 5/9
    elif from_unit == "kelvin" or from_unit == "k":
        celsius = value - 273.15
    else:
        raise ValueError(f"Unknown temperature unit: {from_unit}")
    
    # Then convert from Celsius to target
    if to_unit == "celsius" or to_unit == "c":
        return celsius
    elif to_unit == "fahrenheit" or to_unit == "f":
        return celsius * 9/5 + 32
    elif to_unit == "kelvin" or to_unit == "k":
        return celsius + 273.15
    else:
        raise ValueError(f"Unknown temperature unit: {to_unit}")

# ============== MAIN CONVERTER ==============

def convert_value(value: float, from_unit: str, to_unit: str, category: str) -> float:
    """Main conversion function"""
    category = category.lower()
    
    if category in ["length", "weight"]:
        return convert_standard(value, from_unit, to_unit, category)
    elif category == "temperature":
        return convert_temperature(value, from_unit, to_unit)
    elif category == "currency":
        return convert_currency(value, from_unit, to_unit)
    else:
        raise ValueError(f"Unknown category: {category}")

# ============== HISTORY MANAGEMENT ==============

class ConversionHistory:
    def __init__(self, max_size: int = 100):
        self.history: List[Dict] = []
        self.max_size = max_size
        self.history_file = "conversion_history.json"
        self.load_history()
    
    def add(self, entry: Dict):
        """Add entry to history"""
        entry["timestamp"] = datetime.now().isoformat()
        self.history.append(entry)
        if len(self.history) > self.max_size:
            self.history.pop(0)
        self.save_history()
    
    def get(self, limit: Optional[int] = None) -> List[Dict]:
        """Get history entries"""
        if limit:
            return self.history[-limit:]
        return self.history
    
    def clear(self):
        """Clear history"""
        self.history = []
        self.save_history()
    
    def save_history(self):
        """Save history to file"""
        try:
            with open(self.history_file, "w") as f:
                json.dump(self.history, f, indent=2)
        except:
            pass
    
    def load_history(self):
        """Load history from file"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, "r") as f:
                    self.history = json.load(f)
        except:
            pass

# ============== CSV BATCH PROCESSING ==============

def process_csv_batch(filename: str, output_filename: Optional[str] = None) -> List[Dict]:
    """
    Process batch conversions from CSV file
    Expected CSV columns: value,from_unit,to_unit,category
    """
    results = []
    
    try:
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            
            # Check required columns
            required = ['value', 'from_unit', 'to_unit', 'category']
            if not all(col in reader.fieldnames for col in required):
                print("❌ CSV must have columns: value,from_unit,to_unit,category")
                return results
            
            for row in reader:
                try:
                    value = float(row['value'])
                    from_unit = row['from_unit'].strip()
                    to_unit = row['to_unit'].strip()
                    category = row['category'].strip()
                    
                    result = convert_value(value, from_unit, to_unit, category)
                    
                    result_row = {
                        'original_value': value,
                        'from_unit': from_unit,
                        'to_unit': to_unit,
                        'category': category,
                        'result': result,
                        'status': 'success'
                    }
                    results.append(result_row)
                    
                except Exception as e:
                    results.append({
                        'original_value': row.get('value', 'N/A'),
                        'from_unit': row.get('from_unit', 'N/A'),
                        'to_unit': row.get('to_unit', 'N/A'),
                        'category': row.get('category', 'N/A'),
                        'result': None,
                        'status': f'error: {str(e)}'
                    })
        
        # Write results to file
        if output_filename:
            with open(output_filename, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['original_value', 'from_unit', 'to_unit', 'category', 'result', 'status'])
                writer.writeheader()
                writer.writerows(results)
            print(f"✅ Results saved to {output_filename}")
        
        return results
        
    except FileNotFoundError:
        print(f"❌ File not found: {filename}")
    except Exception as e:
        print(f"❌ Error processing CSV: {e}")
    
    return results

# ============== CLI INTERFACE ==============

def print_available_units():
    """Print available units for each category"""
    print("\n📏 Available Categories and Units:")
    print("-" * 50)
    
    print("\n📐 LENGTH:")
    for unit in sorted(CONVERSION_FACTORS["length"].keys()):
        print(f"  • {unit}")
    
    print("\n⚖️  WEIGHT:")
    for unit in sorted(CONVERSION_FACTORS["weight"].keys()):
        print(f"  • {unit}")
    
    print("\n🌡️  TEMPERATURE:")
    print("  • Celsius, Fahrenheit, Kelvin (or C, F, K)")
    
    print("\n💰 CURRENCY:")
    print("  • Use 3-letter currency codes (USD, EUR, GBP, etc.)")
    print("  • Try: USD, EUR, GBP, JPY, INR, CAD, AUD, etc.")

def interactive_mode(history: ConversionHistory):
    """Interactive CLI mode"""
    print("\n" + "="*60)
    print("🔄 UNIT CONVERTER - Interactive Mode")
    print("="*60)
    print("\nCommands:")
    print("  convert <value> <from> <to> <category>  - Convert units")
    print("  history [n]                             - Show conversion history")
    print("  clear                                   - Clear history")
    print("  units                                   - Show available units")
    print("  batch <filename>                        - Process CSV batch file")
    print("  help                                    - Show this help")
    print("  quit/exit                               - Exit program")
    print("="*60 + "\n")
    
    while True:
        try:
            user_input = input("\n💬 > ").strip()
            
            if not user_input:
                continue
            
            parts = user_input.split()
            command = parts[0].lower()
            
            # === QUIT ===
            if command in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            # === HELP ===
            elif command == 'help':
                print("\n📖 Commands:")
                print("  convert <value> <from_unit> <to_unit> <category>")
                print("  Example: convert 10 meter foot length")
                print("  Example: convert 25 celsius fahrenheit temperature")
                print("  Example: convert 100 usd eur currency\n")
                print("  history [n]  - Show last n conversions")
                print("  clear        - Clear history")
                print("  units        - Show all available units")
                print("  batch <file> - Process CSV file")
                print("  help         - Show this message")
            
            # === UNITS ===
            elif command == 'units':
                print_available_units()
            
            # === HISTORY ===
            elif command == 'history':
                limit = None
                if len(parts) > 1:
                    try:
                        limit = int(parts[1])
                    except:
                        pass
                
                entries = history.get(limit)
                if not entries:
                    print("📭 No conversion history")
                else:
                    print(f"\n📜 Conversion History ({len(entries)} entries):")
                    print("-" * 70)
                    for i, entry in enumerate(entries, 1):
                        print(f"{i}. {entry['value']} {entry['from_unit']} → {entry['result']:.4f} {entry['to_unit']}")
                        print(f"   ({entry['category']}) {entry.get('timestamp', '')}")
                    print("-" * 70)
            
            # === CLEAR HISTORY ===
            elif command == 'clear':
                history.clear()
                print("🗑️  History cleared")
            
            # === BATCH PROCESSING ===
            elif command == 'batch':
                if len(parts) < 2:
                    print("❌ Usage: batch <filename>")
                    continue
                
                filename = parts[1]
                output_filename = f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                results = process_csv_batch(filename, output_filename)
                
                if results:
                    success_count = sum(1 for r in results if r['status'] == 'success')
                    print(f"\n📊 Batch processing complete:")
                    print(f"  ✅ Success: {success_count}")
                    print(f"  ❌ Errors: {len(results) - success_count}")
            
            # === CONVERT ===
            elif command == 'convert':
                if len(parts) < 5:
                    print("❌ Usage: convert <value> <from_unit> <to_unit> <category>")
                    continue
                
                try:
                    value = float(parts[1])
                    from_unit = parts[2]
                    to_unit = parts[3]
                    category = parts[4]
                    
                    result = convert_value(value, from_unit, to_unit, category)
                    
                    # Print result
                    print(f"\n✅ {value} {from_unit} = {result:.6f} {to_unit}")
                    print(f"   Category: {category}")
                    
                    # Add to history
                    history.add({
                        'value': value,
                        'from_unit': from_unit,
                        'to_unit': to_unit,
                        'category': category,
                        'result': result
                    })
                    
                except ValueError as e:
                    print(f"❌ Error: {e}")
                except Exception as e:
                    print(f"❌ Unexpected error: {e}")
            
            else:
                print(f"❌ Unknown command: {command}")
                print("Type 'help' for available commands")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

# ============== MAIN ==============

def main():
    """Main entry point"""
    # Load currency cache
    load_currency_cache()
    
    # Initialize history
    history = ConversionHistory()
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        # Command-line mode
        if sys.argv[1] in ['-h', '--help']:
            print("""
Unit Converter - Usage:
  python unit_converter.py                         - Interactive mode
  python unit_converter.py convert <value> <from> <to> <category>  - Direct conversion
  python unit_converter.py batch <filename>       - Batch conversion from CSV
  python unit_converter.py units                  - List all units
  python unit_converter.py history [n]            - Show conversion history
            """)
        elif sys.argv[1] == 'units':
            print_available_units()
        elif sys.argv[1] == 'history':
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else None
            entries = history.get(limit)
            for entry in entries:
                print(f"{entry['value']} {entry['from_unit']} → {entry['result']} {entry['to_unit']}")
        elif sys.argv[1] == 'batch' and len(sys.argv) > 2:
            output = f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            process_csv_batch(sys.argv[2], output)
        elif sys.argv[1] == 'convert' and len(sys.argv) >= 6:
            try:
                value = float(sys.argv[2])
                result = convert_value(value, sys.argv[3], sys.argv[4], sys.argv[5])
                print(f"{value} {sys.argv[3]} = {result} {sys.argv[4]}")
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("Unknown command. Use --help for usage.")
    else:
        # Interactive mode
        interactive_mode(history)
        
        # Save cache on exit
        save_currency_cache()

if __name__ == "__main__":
    main()