# ==================== FILE HANDLING - ADVANCED & MISCELLANEOUS OPERATIONS ====================

# 1. FILE & DIRECTORY OPERATIONS (os module)
import os
import shutil

# Check if file exists
if os.path.exists('file.txt'):
    print("File exists")

# Get file size
size = os.path.getsize('file.txt')
print(f"Size: {size} bytes")

# Get file info
stat = os.stat('file.txt')
print(f"Modified: {stat.st_mtime}")
print(f"Created: {stat.st_ctime}")
print(f"Permissions: {stat.st_mode}")

# Rename file
os.rename('old_name.txt', 'new_name.txt')

# Delete file
os.remove('file.txt')

# Copy file
shutil.copy('source.txt', 'destination.txt')
shutil.copy2('source.txt', 'destination.txt')  # Preserves metadata

# Move file
shutil.move('source.txt', 'new_location/source.txt')

# Create directory
os.mkdir('new_folder')
os.makedirs('parent/child/grandchild')  # Create nested directories

# List files in directory
files = os.listdir('.')
for file in files:
    print(file)

# Get current working directory
cwd = os.getcwd()
print(f"Current directory: {cwd}")

# Change directory
os.chdir('/path/to/directory')

# 2. FILE METADATA & PERMISSIONS
import stat

# Check if file is readable/writable
if os.access('file.txt', os.R_OK):
    print("Readable")
if os.access('file.txt', os.W_OK):
    print("Writable")
if os.access('file.txt', os.X_OK):
    print("Executable")

# Change file permissions
os.chmod('file.txt', 0o644)  # rw-r--r--
os.chmod('file.txt', stat.S_IRWXU)  # Read, write, execute for owner

# Get file extension and basename
filename = 'path/to/file.txt'
basename = os.path.basename(filename)  # 'file.txt'
dirname = os.path.dirname(filename)  # 'path/to'
name, ext = os.path.splitext(basename)  # 'file', '.txt'

# 3. WORKING WITH PATHS (pathlib - Modern approach)
from pathlib import Path

# Create Path object
path = Path('file.txt')
path = Path('/absolute/path/file.txt')
path = Path.cwd() / 'folder' / 'file.txt'  # Join paths

# Read and write using pathlib
path.write_text('Hello World')  # Write text
content = path.read_text()  # Read text
path.write_bytes(b'Binary data')  # Write binary
data = path.read_bytes()  # Read binary

# Path operations
path.exists()  # Check if exists
path.is_file()  # Is it a file?
path.is_dir()  # Is it a directory?
path.mkdir(parents=True, exist_ok=True)  # Create directory
path.unlink()  # Delete file
path.rename('new_name.txt')  # Rename
path.name  # 'file.txt'
path.stem  # 'file'
path.suffix  # '.txt'
path.parent  # Parent directory

# Iterate through directory
for file in Path('.').iterdir():
    if file.is_file():
        print(f"File: {file.name}")
    elif file.is_dir():
        print(f"Directory: {file.name}")

# Glob pattern matching
for py_file in Path('.').glob('*.py'):
    print(py_file)

for txt_file in Path('.').rglob('*.txt'):  # Recursive
    print(txt_file)

# 4. TEMPORARY FILES
import tempfile

# Create temporary file (auto-deleted)
with tempfile.NamedTemporaryFile(mode='w', delete=True) as tmp:
    tmp.write('Temporary data')
    tmp.flush()
    print(f"Temp file: {tmp.name}")
    # File auto-deleted after block

# Create temporary directory
with tempfile.TemporaryDirectory() as tmpdir:
    print(f"Temp directory: {tmpdir}")
    # Auto-deleted after block

# Create permanent temp file
tmp = tempfile.mkstemp(suffix='.txt', prefix='temp_')
os.close(tmp[0])  # Close file descriptor
print(f"Temp file: {tmp[1]}")

# 5. FILE LOCKING (Prevent simultaneous access)
import fcntl  # Linux/Unix only

# import portalocker  # Cross-platform (install: pip install portalocker)

# Using fcntl (Linux/Unix)
with open('file.txt', 'r+') as file:
    fcntl.flock(file, fcntl.LOCK_EX)  # Exclusive lock
    # Read/Write operations
    fcntl.flock(file, fcntl.LOCK_UN)  # Unlock

# Using portalocker (Cross-platform)
# import portalocker
# with open('file.txt', 'r+') as file:
#     portalocker.lock(file, portalocker.LOCK_EX)
#     # Read/Write operations

# 6. FILE COMPRESSION
import gzip
import zipfile
import tarfile

# GZip compression
with open('file.txt', 'rb') as f_in:
    with gzip.open('file.txt.gz', 'wb') as f_out:
        f_out.writelines(f_in)

# Read gzip file
with gzip.open('file.txt.gz', 'rt') as file:
    content = file.read()

# ZIP file operations
with zipfile.ZipFile('archive.zip', 'w') as zipf:
    zipf.write('file1.txt')
    zipf.write('file2.txt')
    zipf.write('folder/', arcname='folder/')  # Add directory

# Extract ZIP
with zipfile.ZipFile('archive.zip', 'r') as zipf:
    zipf.extractall('extracted_folder')
    zipf.extract('file1.txt', 'extracted_folder')

# Tar file operations
with tarfile.open('archive.tar.gz', 'w:gz') as tar:
    tar.add('file1.txt')
    tar.add('folder')

with tarfile.open('archive.tar.gz', 'r:gz') as tar:
    tar.extractall('extracted_folder')

# 7. FILE WATCHING (Monitor file changes)
# Install: pip install watchdog
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler
#
# class MyHandler(FileSystemEventHandler):
#     def on_modified(self, event):
#         if event.src_path.endswith('.txt'):
#             print(f"File modified: {event.src_path}")
#
# observer = Observer()
# observer.schedule(MyHandler(), path='.')
# observer.start()
# # ... keep running ...
# observer.stop()

# 8. MEMORY-MAPPED FILES (For very large files)
import mmap

with open('large_file.txt', 'r+b') as file:
    with mmap.mmap(file.fileno(), 0) as mmapped:
        # Read data
        data = mmapped.read(100)
        # Modify data
        mmapped[0:5] = b'Hello'
        # Search
        pos = mmapped.find(b'search_text')

# 9. FILE ENCODING DETECTION
# Install: pip install chardet
# import chardet
#
# with open('unknown_encoding.txt', 'rb') as file:
#     raw_data = file.read()
#     result = chardet.detect(raw_data)
#     encoding = result['encoding']
#     print(f"Detected encoding: {encoding}")
#
# with open('unknown_encoding.txt', 'r', encoding=encoding) as file:
#     content = file.read()

# 10. STREAMING (Reading from stdin, writing to stdout)
import sys

# Read from stdin
data = sys.stdin.read()
print("Received:", data)

# Write to stderr
sys.stderr.write("Error message\n")

# Pipe operations
# cat file.txt | python script.py
# python script.py > output.txt

# 11. FILE COMPARISON
import filecmp

# Compare two files
if filecmp.cmp('file1.txt', 'file2.txt'):
    print("Files are identical")
else:
    print("Files differ")

# Compare directories
comparison = filecmp.dircmp('dir1', 'dir2')
print(f"Files only in dir1: {comparison.left_only}")
print(f"Files only in dir2: {comparison.right_only}")
print(f"Common files: {comparison.common}")
print(f"Different files: {comparison.diff_files}")

# 12. FILE HASHING (Checksum)
import hashlib


def file_hash(filename, algorithm='md5'):
    hash_func = hashlib.new(algorithm)
    with open(filename, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b''):
            hash_func.update(chunk)
    return hash_func.hexdigest()


print(f"MD5: {file_hash('file.txt', 'md5')}")
print(f"SHA256: {file_hash('file.txt', 'sha256')}")

# 13. FILE DESCRIPTORS (Low-level operations)
import os

# Open using file descriptor
fd = os.open('file.txt', os.O_RDWR | os.O_CREAT)
os.write(fd, b'Write using descriptor')
os.lseek(fd, 0, os.SEEK_SET)  # Seek to beginning
data = os.read(fd, 100)
os.close(fd)

# 14. READING FILES FROM URL/Internet
import urllib.request
import requests  # pip install requests

# Using urllib
with urllib.request.urlopen('https://example.com/file.txt') as response:
    content = response.read().decode('utf-8')
    print(content)

# Using requests (easier)
response = requests.get('https://example.com/file.txt')
print(response.text)

# Download file
response = requests.get('https://example.com/file.txt')
with open('downloaded.txt', 'wb') as file:
    file.write(response.content)


# 15. FILE SPLITTING AND MERGING
def split_file(filename, chunk_size=1024 * 1024):  # 1MB chunks
    with open(filename, 'rb') as file:
        index = 0
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            with open(f'{filename}.part{index}', 'wb') as chunk_file:
                chunk_file.write(chunk)
            index += 1


def merge_files(base_filename, num_parts):
    with open(f'{base_filename}.merged', 'wb') as output:
        for i in range(num_parts):
            with open(f'{base_filename}.part{i}', 'rb') as part:
                output.write(part.read())


# 16. READING CONFIG FILES
import configparser

# Read INI file
config = configparser.ConfigParser()
config.read('config.ini')

# Access values
db_host = config.get('Database', 'host')
db_port = config.getint('Database', 'port')
debug = config.getboolean('Settings', 'debug')

# Write config
config['Database'] = {'host': 'localhost', 'port': '5432'}
config['Settings'] = {'debug': 'True'}
with open('config.ini', 'w') as file:
    config.write(file)

# 17. PICKLE (Python object serialization)
import pickle

# Save Python objects
data = {'name': 'Alice', 'age': 30, 'scores': [95, 87, 92]}
with open('data.pkl', 'wb') as file:
    pickle.dump(data, file)

# Load Python objects
with open('data.pkl', 'rb') as file:
    loaded_data = pickle.load(file)
    print(loaded_data)

# 18. WORKING WITH SYMLINKS
import os

# Create symbolic link
os.symlink('original.txt', 'link.txt')  # Unix only

# Check if symlink
if os.path.islink('link.txt'):
    print("It's a symlink")
    target = os.readlink('link.txt')
    print(f"Points to: {target}")

# 19. FILE CURSOR OPERATIONS
with open('file.txt', 'r+') as file:
    print(file.tell())  # Current position
    file.seek(5)  # Move to position 5
    print(file.read(10))  # Read 10 chars from position 5
    file.seek(0, 2)  # Move to end (0=start, 1=current, 2=end)
    file.write('End of file')


# 20. READING FILE BACKWARDS
def read_last_n_lines(filename, n=10):
    with open(filename, 'r') as file:
        lines = file.readlines()
        return lines[-n:]


def read_reverse(filename):
    with open(filename, 'r') as file:
        for line in reversed(file.readlines()):
            print(line.strip())


# ==================== COMPLETE FILE MODE REFERENCE ====================
"""
READ MODES:
'r'   - Read (default)
'rb'  - Read binary
'r+'  - Read and write
'rb+' - Read and write binary

WRITE MODES:
'w'   - Write (overwrites)
'wb'  - Write binary
'w+'  - Write and read
'wb+' - Write and read binary

APPEND MODES:
'a'   - Append
'ab'  - Append binary
'a+'  - Append and read
'ab+' - Append and read binary

SPECIAL MODES:
'x'   - Exclusive create (fail if exists)
'xb'  - Exclusive binary create
'x+'  - Exclusive create and read
'xt'  - Exclusive create text
"""

# ==================== BEST PRACTICES SUMMARY ====================
"""
✅ Always use 'with open()' - automatic cleanup
✅ Specify encoding='utf-8' for text files
✅ Use pathlib for modern path handling
✅ Handle exceptions (FileNotFoundError, PermissionError, etc.)
✅ Use buffered reading for large files
✅ Use tempfile for temporary files
✅ Close files explicitly if not using 'with'
✅ Use binary mode for non-text files
✅ Use proper error handling for file operations
✅ Create backup before overwriting important files
✅ Use file locking for concurrent access
✅ Use file hashing for integrity checks
✅ Use configparser for configuration files
✅ Use pickle only for trusted data
✅ Use JSON for data exchange between different languages
"""