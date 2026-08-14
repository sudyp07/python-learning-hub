# ==================== FILE WRITING IN PYTHON - COMPLETE REFERENCE ====================

# 1. BASIC FILE WRITING
with open('file.txt', 'w') as file:
    file.write('Hello World!')                    # Write string
    file.write('\nSecond line')                   # Write with newline

with open('file.txt', 'w') as file:
    lines = ['Line 1\n', 'Line 2\n', 'Line 3\n']
    file.writelines(lines)                        # Write list of strings

# 2. DIFFERENT WRITE MODES
with open('file.txt', 'w') as file:               # 'w' - Write (overwrites)
    file.write('New content')

with open('file.txt', 'a') as file:               # 'a' - Append (adds to end)
    file.write('\nAppended line')

with open('file.txt', 'x') as file:               # 'x' - Exclusive create (fails if exists)
    file.write('New file content')

with open('file.txt', 'r+') as file:              # 'r+' - Read and write
    content = file.read()
    file.write('\nAppended while reading')

# 3. WRITING DIFFERENT DATA TYPES
# String
with open('file.txt', 'w') as file:
    file.write('Hello')

# Integer/Float (convert to string)
with open('file.txt', 'w') as file:
    file.write(str(42))
    file.write('\n' + str(3.14))

# List
with open('file.txt', 'w') as file:
    my_list = ['apple', 'banana', 'cherry']
    for item in my_list:
        file.write(item + '\n')

# Dictionary (JSON)
import json
data = {'name': 'John', 'age': 30, 'city': 'NY'}
with open('data.json', 'w') as file:
    json.dump(data, file, indent=4)               # Pretty print JSON

# CSV
import csv
data = [['Name', 'Age'], ['Alice', 25], ['Bob', 30]]
with open('data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

# 4. ERROR HANDLING
try:
    with open('file.txt', 'w') as file:
        file.write('Content')
except PermissionError:
    print("Permission denied!")
except IOError as e:
    print(f"IO Error: {e}")
except Exception as e:
    print(f"Error: {e}")

# 5. WRITING WITH ENCODING
with open('file.txt', 'w', encoding='utf-8') as file:
    file.write('Unicode text: 你好, 世界')

# 6. BINARY FILE WRITING
with open('file.bin', 'wb') as file:              # 'wb' - Write binary
    file.write(b'Binary data')
    file.write(bytes([65, 66, 67]))               # Write bytes

# 7. WRITING LARGE FILES (Chunk by chunk)
def write_large_file(file_path, data_generator):
    with open(file_path, 'w') as file:
        for chunk in data_generator:
            file.write(chunk)

# Example generator
def generate_data():
    for i in range(1000000):
        yield f"Line {i}\n"

write_large_file('large.txt', generate_data())

# 8. WRITING WITH FORMATTING
name, age = 'Alice', 25
with open('file.txt', 'w') as file:
    file.write(f"Name: {name}, Age: {age}\n")     # f-string
    file.write("Name: {}, Age: {}\n".format(name, age))  # format()
    file.write("Name: %s, Age: %d\n" % (name, age))      # % formatting

# 9. SAFE WRITING (Temporary file then rename)
import os
import tempfile

def safe_write(filename, content):
    temp_file = filename + '.tmp'
    try:
        with open(temp_file, 'w') as f:
            f.write(content)
        os.replace(temp_file, filename)            # Atomic operation
    except Exception:
        if os.path.exists(temp_file):
            os.remove(temp_file)
        raise

safe_write('important.txt', 'Critical data')

# 10. WRITING MULTIPLE FILES
with open('file1.txt', 'w') as f1, open('file2.txt', 'w') as f2:
    f1.write('Content for file 1')
    f2.write('Content for file 2')

# 11. FLUSH AND CLOSE (Manual control)
file = open('file.txt', 'w')
file.write('Data')
file.flush()                                      # Force write to disk
# ... more operations ...
file.close()                                      # Manual close (not recommended)

# 12. APPEND VS WRITE DEMO
# Write mode - overwrites everything
with open('file.txt', 'w') as file:
    file.write('Fresh start\n')

# Append mode - adds to existing
with open('file.txt', 'a') as file:
    file.write('Added at end\n')

# ==================== QUICK REFERENCE ====================
"""
FILE MODES:
- 'w'  → Write (overwrites existing)
- 'a'  → Append (adds to end)
- 'x'  → Exclusive create (fails if exists)
- 'r+' → Read and write
- 'wb' → Write binary
- 'w+' → Write and read

METHODS:
- write(str)      → Write string
- writelines(list)→ Write list of strings
- flush()         → Force write to disk

BEST PRACTICES:
✓ Use 'with open()' for automatic closing
✓ Use 'w' for new files, 'a' for appending
✓ Handle exceptions properly
✓ Use JSON for structured data
✓ Consider safe_write pattern for critical data
✓ Always specify encoding='utf-8' for text
"""