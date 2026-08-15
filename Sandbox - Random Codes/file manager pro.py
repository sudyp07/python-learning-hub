# ==================== FILE MANAGER PRO - COMPLETE PROJECT ====================
# A comprehensive file management system with GUI and CLI interfaces

import os
import shutil
import json
import csv
import pickle
import hashlib
import datetime
import zipfile
import gzip
import tempfile
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
import logging
from dataclasses import dataclass, asdict
from enum import Enum


# ==================== CONFIGURATION ====================
class Config:
    APP_NAME = "FileManager Pro"
    VERSION = "1.0.0"
    LOG_FILE = "file_manager.log"
    CONFIG_FILE = "config.json"
    BACKUP_DIR = "backups"

    @classmethod
    def setup(cls):
        """Initialize application directories and logging"""
        # Create necessary directories
        Path(cls.BACKUP_DIR).mkdir(exist_ok=True)

        # Setup logging
        logging.basicConfig(
            filename=cls.LOG_FILE,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

        # Load or create config
        if not Path(cls.CONFIG_FILE).exists():
            default_config = {
                "theme": "dark",
                "auto_backup": True,
                "backup_interval": 3600,
                "max_history": 100
            }
            with open(cls.CONFIG_FILE, 'w') as f:
                json.dump(default_config, f, indent=4)


# ==================== DATA CLASSES ====================
@dataclass
class FileInfo:
    """Represents file metadata"""
    name: str
    path: str
    size: int
    modified: str
    created: str
    is_dir: bool
    extension: str
    hash: Optional[str] = None

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_path(cls, path: Path) -> 'FileInfo':
        """Create FileInfo from path object"""
        stat = path.stat()
        return cls(
            name=path.name,
            path=str(path),
            size=stat.st_size,
            modified=datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
            created=datetime.datetime.fromtimestamp(stat.st_ctime).isoformat(),
            is_dir=path.is_dir(),
            extension=path.suffix if path.is_file() else '',
            hash=None
        )


@dataclass
class OperationResult:
    """Result of a file operation"""
    success: bool
    message: str
    data: Optional[Any] = None
    error: Optional[str] = None


# ==================== CORE FILE MANAGER ====================
class FileManager:
    """Main file management class with comprehensive operations"""

    def __init__(self):
        self.history: List[Dict] = []
        self.current_dir = Path.cwd()
        Config.setup()
        self.logger = logging.getLogger(__name__)

    # ========== BASIC FILE OPERATIONS ==========

    def create_file(self, filename: str, content: str = '', encoding: str = 'utf-8') -> OperationResult:
        """Create a new file with optional content"""
        try:
            file_path = self.current_dir / filename
            if file_path.exists():
                return OperationResult(False, f"File {filename} already exists")

            with open(file_path, 'w', encoding=encoding) as f:
                f.write(content)

            self._add_history('create', filename)
            self.logger.info(f"Created file: {filename}")
            return OperationResult(True, f"File {filename} created successfully")
        except Exception as e:
            self.logger.error(f"Error creating file {filename}: {e}")
            return OperationResult(False, f"Error creating file", error=str(e))

    def read_file(self, filename: str, encoding: str = 'utf-8') -> OperationResult:
        """Read file content"""
        try:
            file_path = self.current_dir / filename
            if not file_path.exists():
                return OperationResult(False, f"File {filename} not found")

            if file_path.is_dir():
                return OperationResult(False, f"{filename} is a directory")

            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()

            self._add_history('read', filename)
            self.logger.info(f"Read file: {filename}")
            return OperationResult(True, "File read successfully", data=content)
        except UnicodeDecodeError:
            # Try binary mode for non-text files
            try:
                with open(file_path, 'rb') as f:
                    content = f.read()
                return OperationResult(True, "Binary file read successfully", data=content)
            except Exception as e:
                return OperationResult(False, f"Error reading file", error=str(e))
        except Exception as e:
            self.logger.error(f"Error reading file {filename}: {e}")
            return OperationResult(False, f"Error reading file", error=str(e))

    def write_file(self, filename: str, content: str, mode: str = 'w', encoding: str = 'utf-8') -> OperationResult:
        """Write content to file"""
        try:
            file_path = self.current_dir / filename

            # Create backup before overwriting
            if file_path.exists() and mode == 'w':
                self._backup_file(file_path)

            with open(file_path, mode, encoding=encoding) as f:
                f.write(content)

            self._add_history('write', filename)
            self.logger.info(f"Wrote to file: {filename}")
            return OperationResult(True, f"Content written to {filename}")
        except Exception as e:
            self.logger.error(f"Error writing file {filename}: {e}")
            return OperationResult(False, f"Error writing file", error=str(e))

    def append_file(self, filename: str, content: str, encoding: str = 'utf-8') -> OperationResult:
        """Append content to file"""
        return self.write_file(filename, content, mode='a', encoding=encoding)

    def delete_file(self, filename: str) -> OperationResult:
        """Delete a file or directory"""
        try:
            file_path = self.current_dir / filename
            if not file_path.exists():
                return OperationResult(False, f"{filename} not found")

            # Create backup before deletion
            self._backup_file(file_path)

            if file_path.is_dir():
                shutil.rmtree(file_path)
            else:
                file_path.unlink()

            self._add_history('delete', filename)
            self.logger.info(f"Deleted: {filename}")
            return OperationResult(True, f"Deleted {filename} successfully")
        except Exception as e:
            self.logger.error(f"Error deleting {filename}: {e}")
            return OperationResult(False, f"Error deleting", error=str(e))

    def rename_file(self, old_name: str, new_name: str) -> OperationResult:
        """Rename a file or directory"""
        try:
            old_path = self.current_dir / old_name
            new_path = self.current_dir / new_name

            if not old_path.exists():
                return OperationResult(False, f"{old_name} not found")
            if new_path.exists():
                return OperationResult(False, f"{new_name} already exists")

            # Create backup before rename
            self._backup_file(old_path)

            old_path.rename(new_path)

            self._add_history('rename', f"{old_name} -> {new_name}")
            self.logger.info(f"Renamed: {old_name} to {new_name}")
            return OperationResult(True, f"Renamed successfully")
        except Exception as e:
            self.logger.error(f"Error renaming {old_name}: {e}")
            return OperationResult(False, f"Error renaming", error=str(e))

    def copy_file(self, source: str, destination: str) -> OperationResult:
        """Copy a file or directory"""
        try:
            source_path = self.current_dir / source
            dest_path = self.current_dir / destination

            if not source_path.exists():
                return OperationResult(False, f"Source {source} not found")

            if source_path.is_dir():
                shutil.copytree(source_path, dest_path)
            else:
                shutil.copy2(source_path, dest_path)

            self._add_history('copy', f"{source} -> {destination}")
            self.logger.info(f"Copied: {source} to {destination}")
            return OperationResult(True, f"Copied successfully")
        except Exception as e:
            self.logger.error(f"Error copying: {e}")
            return OperationResult(False, f"Error copying", error=str(e))

    def move_file(self, source: str, destination: str) -> OperationResult:
        """Move a file or directory"""
        try:
            source_path = self.current_dir / source
            dest_path = self.current_dir / destination

            if not source_path.exists():
                return OperationResult(False, f"Source {source} not found")

            # Create backup before move
            self._backup_file(source_path)

            shutil.move(str(source_path), str(dest_path))

            self._add_history('move', f"{source} -> {destination}")
            self.logger.info(f"Moved: {source} to {destination}")
            return OperationResult(True, f"Moved successfully")
        except Exception as e:
            self.logger.error(f"Error moving: {e}")
            return OperationResult(False, f"Error moving", error=str(e))

    # ========== DIRECTORY OPERATIONS ==========

    def list_directory(self, path: Optional[str] = None) -> OperationResult:
        """List contents of a directory"""
        try:
            target_path = Path(path) if path else self.current_dir

            if not target_path.exists():
                return OperationResult(False, f"Path {target_path} not found")

            if not target_path.is_dir():
                return OperationResult(False, f"{target_path} is not a directory")

            files = []
            for item in target_path.iterdir():
                file_info = FileInfo.from_path(item)
                files.append(file_info.to_dict())

            return OperationResult(True, "Directory listed successfully", data=files)
        except Exception as e:
            self.logger.error(f"Error listing directory: {e}")
            return OperationResult(False, f"Error listing directory", error=str(e))

    def create_directory(self, dirname: str) -> OperationResult:
        """Create a new directory"""
        try:
            dir_path = self.current_dir / dirname
            if dir_path.exists():
                return OperationResult(False, f"Directory {dirname} already exists")

            dir_path.mkdir(parents=True)

            self._add_history('mkdir', dirname)
            self.logger.info(f"Created directory: {dirname}")
            return OperationResult(True, f"Directory {dirname} created successfully")
        except Exception as e:
            self.logger.error(f"Error creating directory: {e}")
            return OperationResult(False, f"Error creating directory", error=str(e))

    def change_directory(self, path: str) -> OperationResult:
        """Change current working directory"""
        try:
            new_dir = Path(path)
            if not new_dir.is_absolute():
                new_dir = self.current_dir / new_dir

            if not new_dir.exists():
                return OperationResult(False, f"Path {path} not found")

            if not new_dir.is_dir():
                return OperationResult(False, f"{path} is not a directory")

            self.current_dir = new_dir.resolve()
            self.logger.info(f"Changed directory to: {self.current_dir}")
            return OperationResult(True, f"Changed to {self.current_dir}", data=str(self.current_dir))
        except Exception as e:
            self.logger.error(f"Error changing directory: {e}")
            return OperationResult(False, f"Error changing directory", error=str(e))

    def get_current_directory(self) -> str:
        """Get current working directory"""
        return str(self.current_dir)

    # ========== FILE INFORMATION ==========

    def get_file_info(self, filename: str) -> OperationResult:
        """Get detailed file information"""
        try:
            file_path = self.current_dir / filename
            if not file_path.exists():
                return OperationResult(False, f"{filename} not found")

            # Basic info
            file_info = FileInfo.from_path(file_path)

            # Additional info
            stat = file_path.stat()
            extra_info = {
                "permissions": oct(stat.st_mode)[-3:],
                "owner": stat.st_uid,
                "group": stat.st_gid,
                "inode": stat.st_ino,
                "links": stat.st_nlink,
                "device": stat.st_dev,
                "file_type": "Directory" if file_path.is_dir() else "File",
                "absolute_path": str(file_path.resolve()),
                "parent": str(file_path.parent),
                "is_hidden": file_path.name.startswith('.'),
                "is_symlink": file_path.is_symlink(),
                "is_socket": file_path.is_socket(),
                "is_fifo": file_path.is_fifo(),
                "is_block_device": file_path.is_block_device(),
                "is_char_device": file_path.is_char_device()
            }

            # Calculate hash for files
            if file_path.is_file() and file_path.stat().st_size > 0:
                extra_info["hash_md5"] = self._calculate_hash(file_path, 'md5')
                extra_info["hash_sha256"] = self._calculate_hash(file_path, 'sha256')

            result_data = {**file_info.to_dict(), **extra_info}

            self._add_history('info', filename)
            return OperationResult(True, "File info retrieved", data=result_data)
        except Exception as e:
            self.logger.error(f"Error getting file info: {e}")
            return OperationResult(False, f"Error getting file info", error=str(e))

    def search_files(self, pattern: str, recursive: bool = False) -> OperationResult:
        """Search for files matching pattern"""
        try:
            matches = []
            if recursive:
                for item in self.current_dir.rglob(pattern):
                    matches.append(str(item))
            else:
                for item in self.current_dir.glob(pattern):
                    matches.append(str(item))

            return OperationResult(True, f"Found {len(matches)} matches", data=matches)
        except Exception as e:
            self.logger.error(f"Error searching files: {e}")
            return OperationResult(False, f"Error searching files", error=str(e))

    # ========== FILE COMPRESSION ==========

    def compress_zip(self, filename: str, files: List[str]) -> OperationResult:
        """Compress files to ZIP archive"""
        try:
            zip_path = self.current_dir / f"{filename}.zip"

            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file in files:
                    file_path = self.current_dir / file
                    if file_path.exists():
                        if file_path.is_dir():
                            for item in file_path.rglob('*'):
                                if item.is_file():
                                    zipf.write(item, item.relative_to(self.current_dir))
                        else:
                            zipf.write(file_path, file)

            self._add_history('compress', f"{filename}.zip")
            self.logger.info(f"Created ZIP: {filename}.zip")
            return OperationResult(True, f"ZIP archive created: {filename}.zip")
        except Exception as e:
            self.logger.error(f"Error creating ZIP: {e}")
            return OperationResult(False, f"Error creating ZIP", error=str(e))

    def extract_zip(self, filename: str, extract_to: Optional[str] = None) -> OperationResult:
        """Extract ZIP archive"""
        try:
            zip_path = self.current_dir / filename
            if not zip_path.exists():
                return OperationResult(False, f"ZIP file {filename} not found")

            extract_path = self.current_dir / (extract_to or filename.replace('.zip', ''))
            extract_path.mkdir(exist_ok=True)

            with zipfile.ZipFile(zip_path, 'r') as zipf:
                zipf.extractall(extract_path)

            self._add_history('extract', filename)
            self.logger.info(f"Extracted ZIP: {filename}")
            return OperationResult(True, f"ZIP extracted to {extract_path}")
        except Exception as e:
            self.logger.error(f"Error extracting ZIP: {e}")
            return OperationResult(False, f"Error extracting ZIP", error=str(e))

    def compress_gzip(self, filename: str) -> OperationResult:
        """Compress file to GZIP"""
        try:
            file_path = self.current_dir / filename
            if not file_path.exists():
                return OperationResult(False, f"File {filename} not found")

            gz_path = self.current_dir / f"{filename}.gz"

            with open(file_path, 'rb') as f_in:
                with gzip.open(gz_path, 'wb') as f_out:
                    f_out.writelines(f_in)

            self._add_history('compress', f"{filename}.gz")
            self.logger.info(f"Created GZIP: {filename}.gz")
            return OperationResult(True, f"GZIP created: {filename}.gz")
        except Exception as e:
            self.logger.error(f"Error creating GZIP: {e}")
            return OperationResult(False, f"Error creating GZIP", error=str(e))

    # ========== CSV OPERATIONS ==========

    def read_csv(self, filename: str, delimiter: str = ',') -> OperationResult:
        """Read CSV file"""
        try:
            file_path = self.current_dir / filename
            if not file_path.exists():
                return OperationResult(False, f"CSV file {filename} not found")

            with open(file_path, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter=delimiter)
                data = list(reader)

            return OperationResult(True, f"CSV read successfully", data=data)
        except Exception as e:
            self.logger.error(f"Error reading CSV: {e}")
            return OperationResult(False, f"Error reading CSV", error=str(e))

    def write_csv(self, filename: str, data: List[Dict], fieldnames: Optional[List[str]] = None) -> OperationResult:
        """Write to CSV file"""
        try:
            if not data:
                return OperationResult(False, "No data to write")

            file_path = self.current_dir / filename
            if not fieldnames:
                fieldnames = list(data[0].keys())

            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)

            self._add_history('write_csv', filename)
            self.logger.info(f"Written CSV: {filename}")
            return OperationResult(True, f"CSV written successfully")
        except Exception as e:
            self.logger.error(f"Error writing CSV: {e}")
            return OperationResult(False, f"Error writing CSV", error=str(e))

    # ========== JSON OPERATIONS ==========

    def read_json(self, filename: str) -> OperationResult:
        """Read JSON file"""
        try:
            file_path = self.current_dir / filename
            if not file_path.exists():
                return OperationResult(False, f"JSON file {filename} not found")

            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            return OperationResult(True, f"JSON read successfully", data=data)
        except Exception as e:
            self.logger.error(f"Error reading JSON: {e}")
            return OperationResult(False, f"Error reading JSON", error=str(e))

    def write_json(self, filename: str, data: Any, indent: int = 4) -> OperationResult:
        """Write to JSON file"""
        try:
            file_path = self.current_dir / filename

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=indent, sort_keys=True)

            self._add_history('write_json', filename)
            self.logger.info(f"Written JSON: {filename}")
            return OperationResult(True, f"JSON written successfully")
        except Exception as e:
            self.logger.error(f"Error writing JSON: {e}")
            return OperationResult(False, f"Error writing JSON", error=str(e))

    # ========== BACKUP AND RESTORE ==========

    def _backup_file(self, file_path: Path) -> OperationResult:
        """Create a backup of a file"""
        try:
            if not file_path.exists():
                return OperationResult(False, f"File {file_path} not found")

            backup_dir = Path(Config.BACKUP_DIR)
            backup_dir.mkdir(exist_ok=True)

            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{file_path.name}.{timestamp}.backup"
            backup_path = backup_dir / backup_name

            if file_path.is_dir():
                shutil.copytree(file_path, backup_path)
            else:
                shutil.copy2(file_path, backup_path)

            self.logger.info(f"Backup created: {backup_path}")
            return OperationResult(True, f"Backup created: {backup_name}")
        except Exception as e:
            self.logger.error(f"Error creating backup: {e}")
            return OperationResult(False, f"Error creating backup", error=str(e))

    def restore_backup(self, backup_name: str, target: str) -> OperationResult:
        """Restore a backup file"""
        try:
            backup_path = Path(Config.BACKUP_DIR) / backup_name
            if not backup_path.exists():
                return OperationResult(False, f"Backup {backup_name} not found")

            target_path = self.current_dir / target
            if target_path.exists():
                self._backup_file(target_path)  # Backup existing file before restore

            if backup_path.is_dir():
                shutil.copytree(backup_path, target_path, dirs_exist_ok=True)
            else:
                shutil.copy2(backup_path, target_path)

            self.logger.info(f"Restored backup: {backup_name}")
            return OperationResult(True, f"Backup restored successfully")
        except Exception as e:
            self.logger.error(f"Error restoring backup: {e}")
            return OperationResult(False, f"Error restoring backup", error=str(e))

    def list_backups(self) -> OperationResult:
        """List all available backups"""
        try:
            backup_dir = Path(Config.BACKUP_DIR)
            if not backup_dir.exists():
                return OperationResult(True, "No backups found", data=[])

            backups = []
            for item in backup_dir.iterdir():
                backups.append({
                    "name": item.name,
                    "size": item.stat().st_size,
                    "created": datetime.datetime.fromtimestamp(item.stat().st_ctime).isoformat(),
                    "is_dir": item.is_dir()
                })

            return OperationResult(True, f"Found {len(backups)} backups", data=backups)
        except Exception as e:
            self.logger.error(f"Error listing backups: {e}")
            return OperationResult(False, f"Error listing backups", error=str(e))

    # ========== HELPER METHODS ==========

    def _calculate_hash(self, file_path: Path, algorithm: str = 'sha256') -> str:
        """Calculate file hash"""
        try:
            hash_func = hashlib.new(algorithm)
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    hash_func.update(chunk)
            return hash_func.hexdigest()
        except:
            return "N/A"

    def _add_history(self, operation: str, details: str):
        """Add operation to history"""
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "operation": operation,
            "details": details,
            "path": str(self.current_dir)
        }
        self.history.append(entry)

        # Keep only last N operations
        max_history = 100
        if len(self.history) > max_history:
            self.history = self.history[-max_history:]

    def get_history(self) -> List[Dict]:
        """Get operation history"""
        return self.history

    def clear_history(self):
        """Clear operation history"""
        self.history = []

    # ========== BATCH OPERATIONS ==========

    def batch_rename(self, pattern: str, new_pattern: str) -> OperationResult:
        """Batch rename files matching pattern"""
        try:
            files = list(self.current_dir.glob(pattern))
            if not files:
                return OperationResult(False, f"No files match pattern {pattern}")

            renamed = []
            for file in files:
                new_name = file.name.replace(pattern, new_pattern) if '*' not in pattern else new_pattern
                new_path = file.parent / new_name
                if not new_path.exists():
                    file.rename(new_path)
                    renamed.append(file.name)

            self._add_history('batch_rename', f"{len(renamed)} files")
            return OperationResult(True, f"Renamed {len(renamed)} files", data=renamed)
        except Exception as e:
            self.logger.error(f"Error batch renaming: {e}")
            return OperationResult(False, f"Error batch renaming", error=str(e))

    def batch_delete(self, pattern: str) -> OperationResult:
        """Batch delete files matching pattern"""
        try:
            files = list(self.current_dir.glob(pattern))
            if not files:
                return OperationResult(False, f"No files match pattern {pattern}")

            deleted = []
            for file in files:
                # Create backup before deletion
                self._backup_file(file)
                if file.is_dir():
                    shutil.rmtree(file)
                else:
                    file.unlink()
                deleted.append(file.name)

            self._add_history('batch_delete', f"{len(deleted)} files")
            return OperationResult(True, f"Deleted {len(deleted)} files", data=deleted)
        except Exception as e:
            self.logger.error(f"Error batch deleting: {e}")
            return OperationResult(False, f"Error batch deleting", error=str(e))


# ==================== CLI INTERFACE ====================
class FileManagerCLI:
    """Command-line interface for FileManager"""

    def __init__(self):
        self.manager = FileManager()
        self.commands = {
            'ls': self.cmd_ls,
            'cd': self.cmd_cd,
            'pwd': self.cmd_pwd,
            'cat': self.cmd_cat,
            'touch': self.cmd_touch,
            'echo': self.cmd_echo,
            'rm': self.cmd_rm,
            'mv': self.cmd_mv,
            'cp': self.cmd_cp,
            'mkdir': self.cmd_mkdir,
            'info': self.cmd_info,
            'search': self.cmd_search,
            'zip': self.cmd_zip,
            'unzip': self.cmd_unzip,
            'csv': self.cmd_csv,
            'json': self.cmd_json,
            'backup': self.cmd_backup,
            'history': self.cmd_history,
            'clear': self.cmd_clear,
            'help': self.cmd_help,
            'exit': self.cmd_exit
        }

    def run(self):
        """Run the CLI interface"""
        print(f"\n{'=' * 60}")
        print(f"  {Config.APP_NAME} v{Config.VERSION}")
        print(f"  Type 'help' for commands, 'exit' to quit")
        print(f"{'=' * 60}\n")

        while True:
            try:
                current_dir = self.manager.get_current_directory()
                cmd = input(f"\n{current_dir}> ").strip()

                if not cmd:
                    continue

                parts = cmd.split()
                command = parts[0].lower()
                args = parts[1:] if len(parts) > 1 else []

                if command in self.commands:
                    self.commands[command](args)
                else:
                    print(f"Unknown command: {command}. Type 'help' for available commands.")
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit")
            except Exception as e:
                print(f"Error: {e}")

    # ========== COMMAND IMPLEMENTATIONS ==========

    def cmd_ls(self, args):
        """List directory contents"""
        result = self.manager.list_directory(args[0] if args else None)
        if result.success:
            files = result.data
            if files:
                print("\n{:30} {:10} {:20} {}".format("Name", "Size", "Modified", "Type"))
                print("-" * 70)
                for f in files:
                    size = f"{f['size']:,}" if not f['is_dir'] else "DIR"
                    modified = f['modified'][:10] if f['modified'] else ""
                    file_type = "📁" if f['is_dir'] else f"📄 {f['extension']}"
                    print(f"{f['name']:30} {size:10} {modified:20} {file_type}")
            else:
                print("Directory is empty")
        else:
            print(f"Error: {result.message}")

    def cmd_cd(self, args):
        """Change directory"""
        if not args:
            print("Usage: cd <path>")
            return

        result = self.manager.change_directory(args[0])
        if result.success:
            print(f"Changed to: {result.data}")
        else:
            print(f"Error: {result.message}")

    def cmd_pwd(self, args):
        """Print working directory"""
        print(self.manager.get_current_directory())

    def cmd_cat(self, args):
        """Display file content"""
        if not args:
            print("Usage: cat <filename>")
            return

        result = self.manager.read_file(args[0])
        if result.success:
            if isinstance(result.data, bytes):
                print(f"[Binary file] Size: {len(result.data)} bytes")
            else:
                print("\n" + "=" * 50)
                print(result.data)
                print("=" * 50)
        else:
            print(f"Error: {result.message}")

    def cmd_touch(self, args):
        """Create a new file"""
        if not args:
            print("Usage: touch <filename>")
            return

        result = self.manager.create_file(args[0])
        print(f"✓ {result.message}" if result.success else f"✗ {result.message}")

    def cmd_echo(self, args):
        """Write content to file"""
        if len(args) < 2 or args[0] != '>':
            print("Usage: echo 'content' > filename")
            return

        content = args[1:]
        result = self.manager.write_file(args[2], ' '.join(content))
        print(f"✓ {result.message}" if result.success else f"✗ {result.message}")

    def cmd_rm(self, args):
        """Delete file(s)"""
        if not args:
            print("Usage: rm <filename>")
            return

        for file in args:
            result = self.manager.delete_file(file)
            print(f"{'✓' if result.success else '✗'} {result.message}")

    def cmd_mv(self, args):
        """Move/rename file"""
        if len(args) != 2:
            print("Usage: mv <source> <destination>")
            return

        result = self.manager.move_file(args[0], args[1])
        print(f"✓ {result.message}" if result.success else f"✗ {result.message}")

    def cmd_cp(self, args):
        """Copy file"""
        if len(args) != 2:
            print("Usage: cp <source> <destination>")
            return

        result = self.manager.copy_file(args[0], args[1])
        print(f"✓ {result.message}" if result.success else f"✗ {result.message}")

    def cmd_mkdir(self, args):
        """Create directory"""
        if not args:
            print("Usage: mkdir <dirname>")
            return

        result = self.manager.create_directory(args[0])
        print(f"✓ {result.message}" if result.success else f"✗ {result.message}")

    def cmd_info(self, args):
        """Show file information"""
        if not args:
            print("Usage: info <filename>")
            return

        result = self.manager.get_file_info(args[0])
        if result.success:
            data = result.data
            print(f"\n{'=' * 50}")
            print(f"📄 File: {data['name']}")
            print(f"{'=' * 50}")
            for key, value in data.items():
                if key not in ['name']:
                    print(f"{key:20}: {value}")
        else:
            print(f"Error: {result.message}")

    def cmd_search(self, args):
        """Search for files"""
        if not args:
            print("Usage: search <pattern> [recursive]")
            return

        recursive = len(args) > 1 and args[1].lower() == 'recursive'
        result = self.manager.search_files(args[0], recursive)

        if result.success:
            matches = result.data
            if matches:
                print(f"\nFound {len(matches)} matches:")
                for match in matches:
                    print(f"  📄 {match}")
            else:
                print("No matches found")
        else:
            print(f"Error: {result.message}")

    def cmd_zip(self, args):
        """Create ZIP archive"""
        if len(args) < 2:
            print("Usage: zip <archive_name> <file1> [file2 ...]")
            return

        result = self.manager.compress_zip(args[0], args[1:])
        print(f"✓ {result.message}" if result.success else f"✗ {result.message}")

    def cmd_unzip(self, args):
        """Extract ZIP archive"""
        if not args:
            print("Usage: unzip <filename> [extract_to]")
            return

        extract_to = args[1] if len(args) > 1 else None
        result = self.manager.extract_zip(args[0], extract_to)
        print(f"✓ {result.message}" if result.success else f"✗ {result.message}")

    def cmd_csv(self, args):
        """CSV operations"""
        if len(args) < 2:
            print("Usage: csv <read|write> <filename> [data]")
            return

        if args[0] == 'read':
            result = self.manager.read_csv(args[1])
            if result.success:
                data = result.data
                if data:
                    print(f"\nCSV Data ({len(data)} rows):")
                    headers = data[0].keys()
                    print(" | ".join(headers))
                    print("-" * 50)
                    for row in data[:10]:  # Show first 10 rows
                        print(" | ".join(str(row.get(h, '')) for h in headers))
                    if len(data) > 10:
                        print(f"... and {len(data) - 10} more rows")
                else:
                    print("CSV file is empty")
            else:
                print(f"Error: {result.message}")
        elif args[0] == 'write':
            if len(args) < 3:
                print("Usage: csv write <filename> <json_data>")
                return
            try:
                data = json.loads(' '.join(args[2:]))
                result = self.manager.write_csv(args[1], data)
                print(f"✓ {result.message}" if result.success else f"✗ {result.message}")
            except json.JSONDecodeError:
                print("Error: Invalid JSON data")

    def cmd_json(self, args):
        """JSON operations"""
        if len(args) < 2:
            print("Usage: json <read|write> <filename> [data]")
            return

        if args[0] == 'read':
            result = self.manager.read_json(args[1])
            if result.success:
                print(f"\nJSON Data:")
                print(json.dumps(result.data, indent=2, sort_keys=True))
            else:
                print(f"Error: {result.message}")
        elif args[0] == 'write':
            if len(args) < 3:
                print("Usage: json write <filename> <json_data>")
                return
            try:
                data = json.loads(' '.join(args[2:]))
                result = self.manager.write_json(args[1], data)
                print(f"✓ {result.message}" if result.success else f"✗ {result.message}")
            except json.JSONDecodeError:
                print("Error: Invalid JSON data")

    def cmd_backup(self, args):
        """Backup operations"""
        if not args:
            print("Usage: backup <list|create|restore> [args]")
            return

        if args[0] == 'list':
            result = self.manager.list_backups()
            if result.success:
                backups = result.data
                if backups:
                    print("\nAvailable Backups:")
                    for backup in backups:
                        size = f"{backup['size']:,} bytes" if not backup['is_dir'] else "DIR"
                        print(f"  📦 {backup['name']} ({size}) - {backup['created']}")
                else:
                    print("No backups found")
            else:
                print(f"Error: {result.message}")
        elif args[0] == 'create':
            if len(args) < 2:
                print("Usage: backup create <filename>")
                return
            result = self.manager._backup_file(Path(args[1]))
            print(f"✓ {result.message}" if result.success else f"✗ {result.message}")
        elif args[0] == 'restore':
            if len(args) < 3:
                print("Usage: backup restore <backup_name> <target>")
                return
            result = self.manager.restore_backup(args[1], args[2])
            print(f"✓ {result.message}" if result.success else f"✗ {result.message}")

    def cmd_history(self, args):
        """Show operation history"""
        history = self.manager.get_history()
        if history:
            print("\nOperation History:")
            print("=" * 80)
            for entry in history[-20:]:  # Show last 20
                print(f"[{entry['timestamp'][:19]}] {entry['operation'].upper():10} {entry['details']}")
        else:
            print("No history")

    def cmd_clear(self, args):
        """Clear the screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def cmd_help(self, args):
        """Show help"""
        print(f"""
{Config.APP_NAME} v{Config.VERSION} - Command Reference
{'=' * 60}

File Operations:
  ls [path]          - List directory contents
  cd <path>          - Change directory
  pwd                - Print current directory
  touch <file>       - Create new file
  cat <file>         - Display file content
  echo 'text' > file - Write text to file
  rm <file>          - Delete file/directory
  mv <src> <dest>    - Move/rename file
  cp <src> <dest>    - Copy file/directory
  mkdir <dir>        - Create directory
  info <file>        - Show detailed file info
  search <pattern> [recursive] - Search files

Compression:
  zip <name> <files> - Create ZIP archive
  unzip <file> [dir] - Extract ZIP archive

Data Operations:
  csv read <file>    - Read CSV file
  csv write <file> <data> - Write CSV
  json read <file>   - Read JSON file
  json write <file> <data> - Write JSON

Backup:
  backup list        - List backups
  backup create <file> - Create backup
  backup restore <backup> <target> - Restore backup

System:
  history            - Show operation history
  clear              - Clear screen
  help               - Show this help
  exit               - Exit program

Examples:
  touch myfile.txt
  echo "Hello World" > myfile.txt
  cat myfile.txt
  info myfile.txt
  csv read data.csv
  zip archive file1.txt file2.txt
  backup create important.txt
""")

    def cmd_exit(self, args):
        """Exit the program"""
        print(f"\nGoodbye from {Config.APP_NAME}! 👋")
        exit(0)


# ==================== MAIN ====================
def main():
    """Main entry point"""
    try:
        cli = FileManagerCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\nGoodbye! 👋")
    except Exception as e:
        print(f"Fatal error: {e}")
        logging.error(f"Fatal error: {e}", exc_info=True)


if __name__ == "__main__":
    main()