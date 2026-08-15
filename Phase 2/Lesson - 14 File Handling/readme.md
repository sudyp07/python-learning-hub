```markdown
# 📁 Python File Handling - Complete Guide

> A comprehensive guide to file handling in Python covering everything from basic operations to advanced techniques.

## 📋 Table of Contents
- [Introduction](#introduction)
- [Basic File Operations](#basic-file-operations)
- [Reading Files](#reading-files)
- [Writing Files](#writing-files)
- [File Modes](#file-modes)
- [Advanced Operations](#advanced-operations)
- [Working with Paths](#working-with-paths)
- [Different File Types](#different-file-types)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)
- [Common Use Cases](#common-use-cases)
- [Performance Optimization](#performance-optimization)
- [Troubleshooting](#troubleshooting)
- [Quick Reference](#quick-reference)

## Introduction

Python provides robust file handling capabilities through built-in functions and modules. This guide covers everything from basic file I/O to advanced operations like compression, locking, and monitoring.

### Why File Handling Matters
- Data persistence between program runs
- Configuration management
- Data processing and analysis
- Logging and debugging
- System administration

## Basic File Operations

### Opening Files
```python
# Basic open with context manager (recommended)
with open('file.txt', 'r') as file:
    content = file.read()

# Manual open/close (not recommended)
file = open('file.txt', 'r')
content = file.read()
file.close()
```

### File Modes
| Mode | Description |
|------|-------------|
| `'r'` | Read (default) |
| `'w'` | Write (overwrites) |
| `'a'` | Append |
| `'x'` | Exclusive create |
| `'b'` | Binary mode |
| `'+'` | Read and write |

## Reading Files

### Methods
```python
# 1. Read entire file
with open('file.txt', 'r') as f:
    content = f.read()

# 2. Read line by line (memory efficient)
with open('file.txt', 'r') as f:
    for line in f:
        print(line.strip())

# 3. Read all lines as list
with open('file.txt', 'r') as f:
    lines = f.readlines()

# 4. Read specific characters
with open('file.txt', 'r') as f:
    first_10 = f.read(10)
    f.seek(0)  # Reset position
    single_line = f.readline()
```

### Reading Different File Types
```python
# CSV
import csv
with open('data.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

# JSON
import json
with open('data.json', 'r') as f:
    data = json.load(f)

# Binary
with open('image.jpg', 'rb') as f:
    binary_data = f.read()
```

## Writing Files

### Methods
```python
# Write string
with open('file.txt', 'w') as f:
    f.write('Hello World\n')

# Write multiple lines
with open('file.txt', 'w') as f:
    lines = ['Line 1\n', 'Line 2\n', 'Line 3\n']
    f.writelines(lines)

# Append to file
with open('file.txt', 'a') as f:
    f.write('Appended line\n')

# Write different data types
with open('file.txt', 'w') as f:
    f.write(str(42))          # Integer
    f.write('\n' + str(3.14)) # Float
```

### Structured Data Writing
```python
# JSON
with open('data.json', 'w') as f:
    json.dump({'key': 'value'}, f, indent=4)

# CSV
with open('data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows([['Name', 'Age'], ['Alice', 25]])

# Pickle (Python objects)
import pickle
with open('data.pkl', 'wb') as f:
    pickle.dump({'key': 'value'}, f)
```

## Advanced Operations

### Working with Paths
```python
from pathlib import Path

# Modern path handling
path = Path('folder') / 'file.txt'
path.write_text('Hello')
content = path.read_text()

# Path operations
path.exists()           # Check existence
path.is_file()         # Check if file
path.is_dir()          # Check if directory
path.mkdir(parents=True, exist_ok=True)  # Create directories
path.glob('*.txt')     # Pattern matching
path.rglob('*.py')     # Recursive glob
```

### File System Operations
```python
import os
import shutil

# Basic operations
os.rename('old.txt', 'new.txt')        # Rename
os.remove('file.txt')                   # Delete
os.mkdir('folder')                      # Create directory
os.makedirs('parent/child', exist_ok=True)  # Create nested directories

# Copy and move
shutil.copy('source.txt', 'dest.txt')  # Copy
shutil.move('source.txt', 'folder/')   # Move

# List files
files = os.listdir('.')
for file in files:
    print(file)
```

### File Metadata
```python
import os
import stat

# File info
size = os.path.getsize('file.txt')
mtime = os.path.getmtime('file.txt')   # Modified time

# Permissions
if os.access('file.txt', os.R_OK):
    print("Readable")
os.chmod('file.txt', 0o644)  # rw-r--r--
```

### Large File Processing
```python
# Memory-efficient reading
def process_large_file(filename):
    with open(filename, 'r') as f:
        for line in f:
            yield line.strip()

# Process in chunks
def read_in_chunks(filename, chunk_size=1024):
    with open(filename, 'r') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk

# Stream processing
for chunk in read_in_chunks('large.log'):
    process(chunk)  # Your processing logic
```

### File Compression
```python
import gzip
import zipfile
import tarfile

# GZip
with open('file.txt', 'rb') as f_in:
    with gzip.open('file.txt.gz', 'wb') as f_out:
        f_out.writelines(f_in)

# ZIP
with zipfile.ZipFile('archive.zip', 'w') as zipf:
    zipf.write('file1.txt')
    zipf.write('folder/', arcname='folder/')

# Extract ZIP
with zipfile.ZipFile('archive.zip', 'r') as zipf:
    zipf.extractall('extracted/')
```

### Temporary Files
```python
import tempfile

# Temporary file (auto-deleted)
with tempfile.NamedTemporaryFile(mode='w', delete=True) as tmp:
    tmp.write('Temporary data')
    print(f"Temp file: {tmp.name}")

# Temporary directory
with tempfile.TemporaryDirectory() as tmpdir:
    print(f"Temp directory: {tmpdir}")
```

### File Locking
```python
import fcntl  # Linux/Unix

with open('file.txt', 'r+') as f:
    fcntl.flock(f, fcntl.LOCK_EX)  # Exclusive lock
    # Operations here
    fcntl.flock(f, fcntl.LOCK_UN)  # Unlock
```

### File Hashing
```python
import hashlib

def get_file_hash(filename, algorithm='sha256'):
    hash_func = hashlib.new(algorithm)
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_func.update(chunk)
    return hash_func.hexdigest()

# Usage
print(get_file_hash('file.txt', 'md5'))
print(get_file_hash('file.txt', 'sha256'))
```

## Different File Types

### CSV Files
```python
import csv

# Reading
with open('data.csv', 'r') as f:
    reader = csv.DictReader(f)  # Using dictionaries
    for row in reader:
        print(row['Name'], row['Age'])

# Writing
with open('data.csv', 'w', newline='') as f:
    fieldnames = ['Name', 'Age']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({'Name': 'Alice', 'Age': 25})
```

### JSON Files
```python
import json

# Reading
with open('data.json', 'r') as f:
    data = json.load(f)

# Writing with formatting
with open('data.json', 'w') as f:
    json.dump(data, f, indent=4, sort_keys=True)

# Stream reading (large JSON)
import ijson
with open('large.json', 'rb') as f:
    for item in ijson.items(f, 'items.item'):
        print(item)
```

### XML Files
```python
import xml.etree.ElementTree as ET

# Reading
tree = ET.parse('data.xml')
root = tree.getroot()
for child in root:
    print(child.tag, child.attrib)

# Writing
root = ET.Element('root')
child = ET.SubElement(root, 'child')
child.text = 'Content'
tree = ET.ElementTree(root)
tree.write('output.xml')
```

### Config Files
```python
import configparser

# Reading
config = configparser.ConfigParser()
config.read('config.ini')
db_host = config.get('Database', 'host')
debug = config.getboolean('Settings', 'debug')

# Writing
config['Database'] = {'host': 'localhost', 'port': '5432'}
with open('config.ini', 'w') as f:
    config.write(f)
```

## Error Handling

### Basic Error Handling
```python
try:
    with open('file.txt', 'r') as f:
        content = f.read()
except FileNotFoundError:
    print("File doesn't exist")
except PermissionError:
    print("Permission denied")
except UnicodeDecodeError:
    print("Encoding error")
except IOError as e:
    print(f"I/O Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Safe Write Pattern
```python
import os

def safe_write(filename, content):
    temp_file = filename + '.tmp'
    try:
        with open(temp_file, 'w') as f:
            f.write(content)
        os.replace(temp_file, filename)  # Atomic operation
    except Exception:
        if os.path.exists(temp_file):
            os.remove(temp_file)
        raise
```

## Best Practices

### ✅ DO's
1. **Always use context managers** (`with` statement)
2. **Specify encoding** (UTF-8 for text files)
3. **Handle exceptions** appropriately
4. **Use binary mode** for non-text files
5. **Use streaming** for large files
6. **Close files** (automatic with `with`)
7. **Validate file existence** before operations
8. **Use `pathlib`** for path operations
9. **Use temporary files** when needed
10. **Implement proper logging**

### ❌ DON'Ts
1. Don't ignore exceptions
2. Don't forget to specify encoding
3. Don't read large files entirely into memory
4. Don't hardcode file paths
5. Don't use manual close without try/finally
6. Don't assume file permissions
7. Don't modify files while reading
8. Don't ignore cross-platform issues

## Common Use Cases

### 1. Configuration Management
```python
def load_config(config_file='config.json'):
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}  # Default config
```

### 2. Logging
```python
import logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

### 3. Data Processing Pipeline
```python
def process_pipeline(input_file, output_file):
    with open(input_file, 'r') as infile:
        with open(output_file, 'w') as outfile:
            for line in infile:
                processed = process_line(line)
                outfile.write(processed + '\n')
```

### 4. File Backup
```python
def backup_file(filename):
    import shutil
    from datetime import datetime
    backup_name = f"{filename}.{datetime.now():%Y%m%d_%H%M%S}.bak"
    shutil.copy2(filename, backup_name)
    return backup_name
```

## Performance Optimization

### 1. Buffered Reading
```python
# Use buffered I/O
with open('large.txt', 'r', buffering=8192) as f:  # 8KB buffer
    for line in f:
        process(line)
```

### 2. Batch Processing
```python
def process_batches(filename, batch_size=1000):
    batch = []
    with open(filename, 'r') as f:
        for line in f:
            batch.append(line.strip())
            if len(batch) >= batch_size:
                yield batch
                batch = []
        if batch:
            yield batch
```

### 3. Memory Mapping (For very large files)
```python
import mmap

with open('large_file.bin', 'rb') as f:
    with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
        data = mm.read(1024)  # Read without loading entire file
```

### 4. Asynchronous File I/O
```python
import asyncio
import aiofiles  # pip install aiofiles

async def read_file_async(filename):
    async with aiofiles.open(filename, 'r') as f:
        content = await f.read()
    return content
```

## Troubleshooting

### Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| `FileNotFoundError` | Check file path, ensure file exists |
| `PermissionError` | Check file permissions, run with appropriate privileges |
| `UnicodeDecodeError` | Specify correct encoding, use `'rb'` mode |
| `MemoryError` | Use streaming/chunked reading |
| `IOError: [Errno 24]` | Close unused files, increase file descriptor limit |
| `File busy/used` | Wait or use file locking |
| `Encoding mismatch` | Detect encoding with `chardet` |
| `Slow performance` | Use buffering, chunked reading |
| `Cross-platform issues` | Use `os.path.join()` or `pathlib` |

### Debugging Tips
```python
import logging

# Enable detailed logging
logging.basicConfig(level=logging.DEBUG)

# Log file operations
logger = logging.getLogger(__name__)
logger.debug(f"Opening file: {filename}")
logger.debug(f"File size: {os.path.getsize(filename)}")
```

## Quick Reference

### File Methods
```python
# Reading
file.read()         # Read entire file
file.readline()     # Read one line
file.readlines()    # Read all lines
file.seek(offset)   # Move cursor
file.tell()         # Get cursor position

# Writing
file.write(string)  # Write string
file.writelines(list)  # Write list of strings
file.flush()        # Force write to disk

# Properties
file.name          # File name
file.mode          # File mode
file.closed        # Check if closed
```

### Common Patterns
```python
# Reading all text
with open('file.txt') as f: content = f.read()

# Writing all text
with open('file.txt', 'w') as f: f.write(text)

# Reading lines
with open('file.txt') as f: lines = f.readlines()

# Writing lines
with open('file.txt', 'w') as f: f.writelines(lines)

# Appending
with open('file.txt', 'a') as f: f.write(text)

# Binary read
with open('file.bin', 'rb') as f: data = f.read()

# Binary write
with open('file.bin', 'wb') as f: f.write(data)
```

### Useful File Operations
```python
# Check if file exists
os.path.exists('file.txt')

# Get file size
os.path.getsize('file.txt')

# Get extension
os.path.splitext('file.txt')[1]  # '.txt'

# Join paths
os.path.join('folder', 'file.txt')

# Absolute path
os.path.abspath('file.txt')

# Directory of file
os.path.dirname('path/to/file.txt')

# Current directory
os.getcwd()
```

## 📚 Additional Resources

- [Python Official Documentation](https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files)
- [pathlib Documentation](https://docs.python.org/3/library/pathlib.html)
- [CSV Module](https://docs.python.org/3/library/csv.html)
- [JSON Module](https://docs.python.org/3/library/json.html)
- [Pickle Module](https://docs.python.org/3/library/pickle.html)

## 📝 License

This guide is open-source and available for educational purposes.

---

**⭐ Found this helpful? Give it a star!**
