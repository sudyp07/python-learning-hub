# ==================== FILE READING IN PYTHON - COMPLETE REFERENCE ====================

# 1. BASIC FILE READING
with open('file.txt', 'r') as file:
    content = file.read()                          # Read entire file
    print(content)

with open('file.txt', 'r') as file:
    for line in file:                              # Read line by line (memory efficient)
        print(line.strip())

with open('file.txt', 'r') as file:
    lines = file.readlines()                       # Read all lines into list
    print(lines)

# 2. SPECIFIC READING
with open('file.txt', 'r') as file:
    first_10 = file.read(10)                       # Read first 10 characters
    first_line = file.readline()                   # Read single line
    remaining = file.read()                        # Read rest of file

# 3. ERROR HANDLING
try:
    with open('nonexistent.txt', 'r') as file:
        content = file.read()
except FileNotFoundError:
    print("File not found!")
except PermissionError:
    print("Permission denied!")
except Exception as e:
    print(f"Error: {e}")

# 4. DIFFERENT FILE TYPES
import csv
with open('data.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)

import json
with open('data.json', 'r') as file:
    data = json.load(file)
    print(data)

with open('file.txt', 'r', encoding='utf-8') as file:   # Specify encoding
    content = file.read()

# 5. MULTIPLE FILES
with open('file1.txt', 'r') as f1, open('file2.txt', 'r') as f2:
    content1 = f1.read()
    content2 = f2.read()

# 6. LARGE FILE READING (Memory Efficient)
def read_large_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            yield line.strip()

for line in read_large_file('large_file.txt'):
    print(line)  # Process each line

def read_in_chunks(file_path, chunk_size=1024):
    with open(file_path, 'r') as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            yield chunk

for chunk in read_in_chunks('large_file.txt'):
    print(chunk)  # Process each chunk

# 7. CHECK IF FILE EXISTS BEFORE READING
import os
if os.path.exists('file.txt'):
    with open('file.txt', 'r') as file:
        content = file.read()
else:
    print("File doesn't exist")

# 8. READING WITH POSITION (SEEK/TELL)
with open('file.txt', 'r') as file:
    print(file.tell())        # Current position: 0
    file.read(5)              # Read 5 characters
    print(file.tell())        # Current position: 5
    file.seek(0)              # Go back to start
    print(file.read())        # Read entire file again

# ==================== QUICK REFERENCE ====================
"""
METHODS:
- read()      → Whole file as string
- readline()  → Single line
- readlines() → All lines as list
- for line    → Iterate lines (most memory efficient)

MODES:
- 'r'  → Read (default)
- 'rb' → Read binary
- 'r+' → Read and write

BEST PRACTICES:
✓ Always use 'with open()' for automatic closing
✓ Use encoding='utf-8' for text files
✓ Handle exceptions properly
✓ Use generators for large files
"""