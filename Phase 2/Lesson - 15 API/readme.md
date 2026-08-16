# 📦 API FETCHING IN PYTHON - COMPLETE GUIDE

```markdown
# 🐍 API FETCHING IN PYTHON - COMPLETE GUIDE

A comprehensive guide and implementation for fetching data from REST APIs using Python, with detailed examples using the PokeAPI.

---

## 📋 TABLE OF CONTENTS

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Understanding APIs](#understanding-apis)
- [Project Structure](#project-structure)
- [Code Explanation](#code-explanation)
- [Usage Guide](#usage-guide)
- [API Methods Explained](#api-methods-explained)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)
- [Advanced Topics](#advanced-topics)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## 📌 OVERVIEW

This project demonstrates how to fetch data from REST APIs in Python. Using the popular PokeAPI as an example, it covers:

### ✨ Key Features
- 🔍 Search any Pokémon by name or ID
- 📊 Display detailed statistics and abilities
- 💾 Save data to JSON files
- 🎯 Complete error handling
- 📱 User-friendly interface
- 🚀 Ready-to-use functions

### 🎯 What You'll Learn
- Making HTTP requests
- Handling API responses
- Parsing JSON data
- Error handling and edge cases
- Data visualization and file operations

---

## 🔧 PREREQUISITES

Before you begin, ensure you have:

| Requirement | Details |
|-------------|---------|
| **Python** | Version 3.7+ installed |
| **Knowledge** | Basic Python programming |
| **Internet** | Connection to access API |
| **JSON** | Basic understanding (helpful) |

### Check Python Version
```bash
python --version
# or
python3 --version
```

---

## 📦 INSTALLATION

### Step 1: Install Required Library
```bash
pip install requests
```

### Step 2: Verify Installation
```python
import requests
print(requests.__version__)  # Should display version number
```

### Step 3: Create Project File
Create a new Python file `pokemon_api.py` and copy the code.

---

## 🌐 UNDERSTANDING APIS

### What is an API?
An **API (Application Programming Interface)** is a set of rules that allows different software applications to communicate.

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    CLIENT   │ ──▶│     API     │ ──▶│   SERVER    │
│  (Python)   │ ◀──│   (Waiter)  │ ◀──│  (Kitchen)  │
└─────────────┘    └─────────────┘    └─────────────┘
     You                Waiter             Kitchen
```

### REST API Basics

| Concept | Explanation | Example |
|---------|-------------|---------|
| **Endpoint** | URL where API can be accessed | `https://pokeapi.co/api/v2/pokemon/pikachu` |
| **HTTP Methods** | Actions you can perform | GET, POST, PUT, DELETE |
| **Headers** | Additional information | Authentication, content type |
| **Parameters** | Data sent with request | `?limit=10&offset=5` |
| **Status Codes** | Response indicators | 200=OK, 404=Not Found |

### API Response Structure
```json
{
    "name": "pikachu",
    "height": 4,
    "weight": 60,
    "abilities": [
        {
            "ability": {
                "name": "static"
            }
        }
    ]
}
```

---

## 📁 PROJECT STRUCTURE

```
api-fetching-python/
│
├── 📄 pokemon_api.py          # Main program file
├── 📄 README.md              # This file
├── 📄 requirements.txt       # Python dependencies
│
├── 📁 examples/
│   ├── basic_get.py       # Simple GET request
│   ├── async_fetch.py     # Asynchronous requests
│   └── batch_requests.py  # Multiple API calls
│
├── 📁 data/                  # Saved JSON data
│   └── pikachu_data.json  # Example saved data
│
└── 📁 docs/
    ├── api_reference.md   # Detailed API docs
    └── troubleshooting.md # Common issues
```

---

## 💻 CODE EXPLANATION

### 1. Importing Libraries
```python
import requests  # For making HTTP requests
import json      # For handling JSON data (built-in)
```

### 2. Making a GET Request
```python
def fetch_pokemon_data(pokemon_name):
    """
    Fetch Pokémon data from the API
    
    Args:
        pokemon_name (str): Name of the Pokémon
    
    Returns:
        dict: Pokémon data or None if not found
    """
    # Step 1: Build the URL
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    
    # Step 2: Send request
    response = requests.get(url)
    
    # Step 3: Check response
    if response.status_code == 200:
        # Step 4: Parse JSON
        data = response.json()
        return data
    else:
        return None
```

### 3. Parsing JSON Response
```python
# Accessing basic data
name = data['name']                    # Simple field
height = data['height']                # Simple field

# Accessing nested data
abilities = data['abilities']
for ability in abilities:
    ability_name = ability['ability']['name']  # Nested field

# Accessing array data
stats = data['stats']
for stat in stats:
    stat_name = stat['stat']['name']
    base_value = stat['base_stat']
```

### 4. Error Handling
```python
try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()  # Raises exception for bad status codes
    data = response.json()
except requests.exceptions.ConnectionError:
    print("Network error - check your internet connection")
except requests.exceptions.Timeout:
    print("Request timed out - server is slow")
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
except ValueError:
    print("Invalid JSON response")
```

---

## 🚀 USAGE GUIDE

### Basic Usage

#### 1. Search for a Pokémon
```bash
# Run the program
python pokemon_api.py

# Enter a Pokémon name when prompted
Enter Pokémon name: pikachu
```

#### 2. Using Functions Directly
```python
from pokemon_api import fetch_pokemon_data, display_pokemon_info

# Fetch data
data = fetch_pokemon_data("charizard")

# Display info
display_pokemon_info(data)
```

#### 3. Save Data to File
```python
from pokemon_api import save_pokemon_to_file

data = fetch_pokemon_data("mewtwo")
save_pokemon_to_file(data, "mewtwo_data.json")
```

### Advanced Usage

#### Fetch Multiple Pokémon
```python
pokemon_list = ["pikachu", "charizard", "bulbasaur"]

for name in pokemon_list:
    data = fetch_pokemon_data(name)
    if data:
        print(f"✅ {name}: Level {data['base_experience']}")
    else:
        print(f"❌ {name}: Not found")
```

#### Filter Pokémon by Type
```python
def get_pokemon_by_type(type_name):
    url = f"https://pokeapi.co/api/v2/type/{type_name}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        pokemon_list = []
        for entry in data['pokemon']:
            pokemon_list.append(entry['pokemon']['name'])
        return pokemon_list
    return []

# Example: Get all fire-type Pokémon
fire_pokemon = get_pokemon_by_type("fire")
print(f"🔥 Fire Pokémon: {', '.join(fire_pokemon[:10])}")
```

---

## 📚 API METHODS EXPLAINED

### GET Method
**Purpose**: Retrieve data from the server

```python
response = requests.get(url)
```

| Aspect | Details |
|--------|---------|
| **Use** | Fetching Pokémon data, search queries |
| **Parameters** | URL, headers, query strings |
| **Response** | Data in JSON format |

### POST Method
**Purpose**: Send data to create new resources

```python
data = {"name": "new_pokemon", "type": "electric"}
response = requests.post(url, json=data)
```

| Aspect | Details |
|--------|---------|
| **Use** | Creating new entries, authentication |
| **Data** | Sent in request body |

### PUT vs PATCH
```python
# PUT - Complete update
response = requests.put(url, json={"id": 1, "name": "updated"})

# PATCH - Partial update
response = requests.patch(url, json={"name": "updated"})
```

### DELETE Method
```python
response = requests.delete(url)
```

| Aspect | Details |
|--------|---------|
| **Use** | Removing resources |
| **Note** | Usually requires authentication |

---

## ⚠️ ERROR HANDLING

### Common HTTP Status Codes

| Code | Meaning | How to Handle |
|------|---------|---------------|
| 200 | OK | Process the data |
| 201 | Created | Resource successfully created |
| 400 | Bad Request | Check your parameters |
| 401 | Unauthorized | Add authentication |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 429 | Too Many Requests | Implement rate limiting |
| 500 | Internal Server Error | Retry after delay |

### Error Handling Template
```python
def safe_api_call(url):
    try:
        response = requests.get(url, timeout=10)
        
        # Check status
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print(f"Resource not found: {url}")
        elif response.status_code == 429:
            print("Rate limited - waiting 5 seconds...")
            time.sleep(5)
            return safe_api_call(url)  # Retry
        else:
            print(f"Unexpected status: {response.status_code}")
            
    except requests.Timeout:
        print("Request timed out")
    except requests.ConnectionError:
        print("Network error")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    return None
```

---

## ✅ BEST PRACTICES

### 1. Rate Limiting
```python
import time

def fetch_with_delay(urls, delay=1):
    results = []
    for url in urls:
        response = requests.get(url)
        results.append(response.json())
        time.sleep(delay)  # Be nice to the API
    return results
```

### 2. Caching Responses
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_pokemon(name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name}"
    response = requests.get(url)
    return response.json()
```

### 3. Environment Variables for API Keys
```python
import os

# Set in environment: export API_KEY="your_key_here"
API_KEY = os.getenv('API_KEY')
headers = {'Authorization': f'Bearer {API_KEY}'}
response = requests.get(url, headers=headers)
```

### 4. Request Retries with Exponential Backoff
```python
def request_with_retry(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=5)
            return response.json()
        except requests.RequestException:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
```

---

## 🚀 ADVANCED TOPICS

### 1. Async Requests with Aiohttp
```python
import aiohttp
import asyncio

async def fetch_pokemon(session, name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name}"
    async with session.get(url) as response:
        return await response.json()

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_pokemon(session, name) 
                 for name in ["pikachu", "charizard", "bulbasaur"]]
        results = await asyncio.gather(*tasks)
        return results

# Run: asyncio.run(main())
```

### 2. Data Visualization
```python
import matplotlib.pyplot as plt

def plot_stats(pokemon_data):
    names = []
    values = []
    
    for stat in pokemon_data['stats']:
        names.append(stat['stat']['name'].upper())
        values.append(stat['base_stat'])
    
    plt.figure(figsize=(10, 6))
    plt.bar(names, values)
    plt.title(f"{pokemon_data['name'].upper()} Base Stats")
    plt.ylabel("Base Value")
    plt.show()
```

### 3. Webhook Integration
```python
def setup_webhook(url, callback_url):
    webhook_data = {
        "url": callback_url,
        "events": ["pokemon_created", "pokemon_updated"]
    }
    response = requests.post(f"{url}/webhooks", json=webhook_data)
    return response.status_code == 201
```

---

## 🔧 TROUBLESHOOTING

### Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| **ConnectionError** | Check internet connection, verify URL |
| **Timeout** | Increase timeout parameter, check server status |
| **404 Not Found** | Verify resource name/ID, check API documentation |
| **JSONDecodeError** | Response isn't valid JSON, check content-type header |
| **Rate Limit** | Implement backoff strategy, use caching |
| **SSL Certificate** | Use `verify=False` (not recommended for production) |

### Debugging Tips
```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Log requests
response = requests.get(url)
print(f"Status: {response.status_code}")
print(f"Headers: {response.headers}")
print(f"Content: {response.text[:200]}")  # First 200 chars
```

---

## 🤝 CONTRIBUTING

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add/update tests
5. Submit a pull request

### Development Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/api-fetching-python.git

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/
```

---

## 📄 LICENSE

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📚 RESOURCES

### Official Documentation
- [Requests Library](https://docs.python-requests.org/)
- [PokeAPI Documentation](https://pokeapi.co/docs/v2)
- [REST API Tutorial](https://restfulapi.net/)

### Further Reading
- [HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
- [JSON Format](https://www.json.org/)
- [API Design Best Practices](https://docs.microsoft.com/en-us/azure/architecture/best-practices/api-design)

### Video Tutorials
- [REST APIs in Python](https://www.youtube.com/watch?v=qsrZrgBd-PY)
- [Working with JSON](https://www.youtube.com/watch?v=9N6a-VLBA2c)

---

## ⚡ QUICK REFERENCE CARD

### Common Code Snippets

```python
# GET request with parameters
params = {'limit': 20, 'offset': 10}
response = requests.get(url, params=params)

# POST request with JSON
data = {'name': 'Pikachu', 'type': 'Electric'}
response = requests.post(url, json=data)

# Headers for authentication
headers = {'Authorization': 'Bearer YOUR_TOKEN'}
response = requests.get(url, headers=headers)

# Save response to file
with open('data.json', 'w') as f:
    json.dump(response.json(), f, indent=2)

# Load from file
with open('data.json', 'r') as f:
    data = json.load(f)
```

### API URL Templates

```
# Pokémon API
https://pokeapi.co/api/v2/pokemon/{name_or_id}
https://pokeapi.co/api/v2/type/{type_name}
https://pokeapi.co/api/v2/ability/{ability_name}

# Common Patterns
{base_url}/{resource}/{id}          # Single resource
{base_url}/{resource}?{parameters}  # Collection with filters
{base_url}/{resource}/{id}/{sub}    # Nested resources
```

---

## 📊 COMPLETE CODE EXAMPLE

```python
#!/usr/bin/env python3
"""
=======================================
🐍 POKEMON API FETCHER - COMPLETE CODE
=======================================
A comprehensive example of fetching data from REST APIs
"""

import requests
import json
import time
from typing import Dict, Optional, List

# ============================================
# 1. CORE API FUNCTIONS
# ============================================

def fetch_pokemon_data(pokemon_name: str) -> Optional[Dict]:
    """
    Fetch detailed information about a Pokémon from the PokeAPI
    
    Args:
        pokemon_name (str): Name of the Pokémon (e.g., 'pikachu')
    
    Returns:
        dict: Pokémon data or None if not found
    """
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection Error: Could not connect to API")
    except requests.exceptions.Timeout:
        print(f"❌ Timeout: Server took too long to respond")
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            print(f"❌ Pokémon '{pokemon_name}' not found!")
        else:
            print(f"❌ HTTP Error {response.status_code}: {e}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Request Error: {e}")
    except ValueError:
        print(f"❌ Invalid JSON response")
    
    return None

# ============================================
# 2. DATA DISPLAY FUNCTIONS
# ============================================

def display_pokemon_info(data: Dict) -> None:
    """
    Display formatted Pokémon information
    
    Args:
        data (dict): Pokémon data from the API
    """
    if not data:
        return
    
    print("\n" + "=" * 50)
    print(f"📊 POKÉMON DETAILS")
    print("=" * 50)
    
    # Basic Info
    print(f"🎯 Name: {data['name'].capitalize()}")
    print(f"📏 Height: {data['height']/10:.1f} m")
    print(f"⚖️ Weight: {data['weight']/10:.1f} kg")
    
    # Types
    types = [t['type']['name'].capitalize() for t in data['types']]
    print(f"🏷️ Types: {', '.join(types)}")
    
    # Abilities
    abilities = []
    for a in data['abilities']:
        name = a['ability']['name'].replace('-', ' ').capitalize()
        if a['is_hidden']:
            abilities.append(f"{name} (Hidden)")
        else:
            abilities.append(name)
    print(f"💪 Abilities: {', '.join(abilities)}")
    
    # Stats
    print("\n📈 BASE STATS:")
    stat_names = {
        'hp': 'HP',
        'attack': 'Attack',
        'defense': 'Defense',
        'special-attack': 'Sp. Atk',
        'special-defense': 'Sp. Def',
        'speed': 'Speed'
    }
    
    for stat in data['stats']:
        name = stat['stat']['name']
        value = stat['base_stat']
        display_name = stat_names.get(name, name.capitalize())
        print(f"   {display_name}: {value}")
    
    # Experience
    print(f"\n⭐ Base Experience: {data['base_experience']}")
    
    # Sample Moves
    moves = [m['move']['name'].replace('-', ' ').capitalize() 
             for m in data['moves'][:5]]
    print(f"🎮 Sample Moves: {', '.join(moves)}")
    if len(data['moves']) > 5:
        print(f"   ... and {len(data['moves']) - 5} more moves")
    
    print("=" * 50)

# ============================================
# 3. FILE OPERATIONS
# ============================================

def save_pokemon_to_file(data: Dict, filename: str = None) -> bool:
    """
    Save Pokémon data to a JSON file
    
    Args:
        data (dict): Pokémon data
        filename (str): Optional custom filename
    
    Returns:
        bool: Success status
    """
    if not data:
        return False
    
    if not filename:
        filename = f"{data['name']}_data.json"
    
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"💾 Data saved to {filename}")
        return True
    except Exception as e:
        print(f"⚠️ Could not save file: {e}")
        return False

# ============================================
# 4. BATCH OPERATIONS
# ============================================

def fetch_multiple_pokemon(pokemon_list: List[str]) -> Dict:
    """
    Fetch multiple Pokémon with rate limiting
    
    Args:
        pokemon_list (list): List of Pokémon names
    
    Returns:
        dict: Dictionary of name -> data pairs
    """
    results = {}
    
    for name in pokemon_list:
        print(f"🔍 Fetching {name}...")
        data = fetch_pokemon_data(name)
        if data:
            results[name] = data
        time.sleep(0.5)  # Rate limiting
    
    return results

def get_pokemon_by_type(type_name: str) -> Optional[List[str]]:
    """
    Get all Pokémon of a specific type
    
    Args:
        type_name (str): Type name (e.g., 'fire', 'water')
    
    Returns:
        list: List of Pokémon names
    """
    url = f"https://pokeapi.co/api/v2/type/{type_name.lower()}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        pokemon_list = []
        for entry in data['pokemon']:
            pokemon_list.append(entry['pokemon']['name'])
        
        return pokemon_list
        
    except Exception as e:
        print(f"❌ Error fetching type data: {e}")
        return None

# ============================================
# 5. INTERACTIVE MAIN PROGRAM
# ============================================

def main():
    """Main program loop"""
    print("🐉 POKÉMON API EXPLORER 🐉")
    print("=" * 40)
    print("Commands:")
    print("  - Enter Pokémon name to search")
    print("  - 'batch' to fetch multiple Pokémon")
    print("  - 'type' to search by type")
    print("  - 'quit' to exit")
    print("=" * 40)
    
    while True:
        command = input("\n🔍 Enter command: ").strip().lower()
        
        # Exit
        if command in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
        
        # Batch fetch
        elif command == 'batch':
            names = input("📝 Enter Pokémon names (comma-separated): ").strip()
            pokemon_names = [n.strip() for n in names.split(',')]
            
            if pokemon_names:
                results = fetch_multiple_pokemon(pokemon_names)
                for name, data in results.items():
                    display_pokemon_info(data)
        
        # Search by type
        elif command == 'type':
            type_name = input("🎯 Enter type name: ").strip()
            pokemon_list = get_pokemon_by_type(type_name)
            
            if pokemon_list:
                print(f"\n📊 {len(pokemon_list)} {type_name.upper()}-type Pokémon:")
                # Show first 20
                for i, name in enumerate(pokemon_list[:20], 1):
                    print(f"   {i:2d}. {name.capitalize()}")
                if len(pokemon_list) > 20:
                    print(f"   ... and {len(pokemon_list) - 20} more")
        
        # Single Pokémon search
        else:
            data = fetch_pokemon_data(command)
            if data:
                display_pokemon_info(data)
                
                # Ask to save
                save_choice = input("\n💾 Save to file? (y/n): ").lower()
                if save_choice in ['y', 'yes']:
                    save_pokemon_to_file(data)

# ============================================
# 6. ENTRY POINT
# ============================================

if __name__ == "__main__":
    main()
```

---

## 🎯 COMPLETE USAGE EXAMPLE

```bash
$ python pokemon_api.py

🐉 POKÉMON API EXPLORER 🐉
========================================
Commands:
  - Enter Pokémon name to search
  - 'batch' to fetch multiple Pokémon
  - 'type' to search by type
  - 'quit' to exit
========================================

🔍 Enter command: pikachu

==================================================
📊 POKÉMON DETAILS
==================================================
🎯 Name: Pikachu
📏 Height: 0.4 m
⚖️ Weight: 6.0 kg
🏷️ Types: Electric
💪 Abilities: Static, Lightning rod (Hidden)

📈 BASE STATS:
   HP: 35
   Attack: 55
   Defense: 40
   Sp. Atk: 50
   Sp. Def: 50
   Speed: 90

⭐ Base Experience: 112
🎮 Sample Moves: Mega punch, Pay day, Thunder punch, Swords dance, Mega kick
   ... and many more moves
==================================================

💾 Save to file? (y/n): y
💾 Data saved to pikachu_data.json
```

---

## 🎉 SUMMARY

### ✅ What You've Learned
- Making API requests with Python
- Handling JSON responses
- Error handling and debugging
- Best practices for API usage
- Data visualization and storage

### 📚 Quick Reference

| Task | Code |
|------|------|
| **GET Request** | `response = requests.get(url)` |
| **POST Request** | `response = requests.post(url, json=data)` |
| **Check Status** | `if response.status_code == 200:` |
| **Parse JSON** | `data = response.json()` |
| **Headers** | `headers = {'Authorization': 'Bearer TOKEN'}` |
| **Parameters** | `params = {'limit': 10, 'offset': 5}` |
| **Timeout** | `response = requests.get(url, timeout=5)` |

---

**🐍 Happy API Coding!**

*If you found this guide helpful, please ⭐ star the repository and share!*

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/api-fetching-python/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/api-fetching-python/discussions)
- **Email**: your.email@example.com

---

<div align="center">
  Made with ❤️ by Sudip Hero
</div>
```