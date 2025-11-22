"""
Backup Manager - Creates timestamped snapshots for safe rollback
Part of MayAssistant Repository Restructure Safety System
"""

import os
import shutil
import json
from datetime import datetime
from pathlib import Path
import hashlib


class BackupManager:
    """Manages complete repository backups with integrity verification"""
    
    def __init__(self, repo_root):
        self.repo_root = Path(repo_root)
        self.backup_dir = self.repo_root / ".restructure_backups"
        self.backup_dir.mkdir(exist_ok=True)
        
    def create_backup(self):
        """Create a complete backup of the repository state"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}"
        backup_path = self.backup_dir / backup_name
        
        print(f"🔒 Creating backup: {backup_name}")
        print(f"📂 Backup location: {backup_path}")
        
        # Create backup metadata
        metadata = {
            "timestamp": timestamp,
            "backup_name": backup_name,
            "repo_root": str(self.repo_root),
            "created_at": datetime.now().isoformat(),
            "files_backed_up": []
        }
        
        # Directories to backup
        dirs_to_backup = [
            "api", "dashboard", "dev-portal", "deploy_tmp", 
            "functions", "legacy_v3_functions", "shared",
            "backend", "nova-backend", "eli-backend", "omega-frontend",
            "docs", "infrastructure", "packs", "tests", "cursor",
            ".github", ".cursor", "diagnostics"
        ]
        
        # Files to backup (root level)
        files_to_backup = [
            f for f in os.listdir(self.repo_root) 
            if f.endswith(('.md', '.py', '.sh', '.ps1', '.json', '.txt'))
            and os.path.isfile(self.repo_root / f)
        ]
        
        backup_path.mkdir(parents=True, exist_ok=True)
        
        # Backup directories
        for dir_name in dirs_to_backup:
            src = self.repo_root / dir_name
            if src.exists() and src.is_dir():
                dst = backup_path / dir_name
                print(f"   📁 Backing up: {dir_name}")
                shutil.copytree(src, dst, symlinks=True, ignore=shutil.ignore_patterns(
                    '__pycache__', '*.pyc', 'node_modules', '.git', 
                    'venv', '.venv', '*.egg-info'
                ))
                metadata["files_backed_up"].append(dir_name)
        
        # Backup root files
        for file_name in files_to_backup:
            src = self.repo_root / file_name
            if src.exists() and src.is_file():
                dst = backup_path / file_name
                print(f"   📄 Backing up: {file_name}")
                shutil.copy2(src, dst)
                metadata["files_backed_up"].append(file_name)
        
        # Calculate checksums for verification
        metadata["checksums"] = self._calculate_checksums(backup_path)
        
        # Save metadata
        metadata_path = backup_path / "backup_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"✅ Backup complete: {len(metadata['files_backed_up'])} items backed up")
        print(f"📋 Metadata saved: {metadata_path}")
        
        return backup_name, backup_path
    
    def _calculate_checksums(self, backup_path):
        """Calculate checksums for all files in backup"""
        checksums = {}
        for root, dirs, files in os.walk(backup_path):
            for file in files:
                if file == "backup_metadata.json":
                    continue
                file_path = Path(root) / file
                relative_path = file_path.relative_to(backup_path)
                try:
                    with open(file_path, 'rb') as f:
                        checksums[str(relative_path)] = hashlib.md5(f.read()).hexdigest()
                except Exception as e:
                    print(f"   ⚠️  Could not checksum {relative_path}: {e}")
        return checksums
    
    def list_backups(self):
        """List all available backups"""
        if not self.backup_dir.exists():
            return []
        
        backups = []
        for backup in sorted(self.backup_dir.iterdir(), reverse=True):
            if backup.is_dir() and backup.name.startswith("backup_"):
                metadata_path = backup / "backup_metadata.json"
                if metadata_path.exists():
                    with open(metadata_path, 'r') as f:
                        metadata = json.load(f)
                    backups.append({
                        "name": backup.name,
                        "path": backup,
                        "created_at": metadata.get("created_at"),
                        "files_count": len(metadata.get("files_backed_up", []))
                    })
        return backups
    
    def get_latest_backup(self):
        """Get the most recent backup"""
        backups = self.list_backups()
        return backups[0] if backups else None
    
    def verify_backup(self, backup_name):
        """Verify backup integrity"""
        backup_path = self.backup_dir / backup_name
        metadata_path = backup_path / "backup_metadata.json"
        
        if not metadata_path.exists():
            return False, "Backup metadata not found"
        
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        # Verify checksums
        stored_checksums = metadata.get("checksums", {})
        current_checksums = self._calculate_checksums(backup_path)
        
        if stored_checksums != current_checksums:
            return False, "Checksum mismatch - backup may be corrupted"
        
        return True, "Backup verified successfully"


if __name__ == "__main__":
    # Test the backup manager
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python backup_manager.py <repo_root>")
        sys.exit(1)
    
    repo_root = sys.argv[1]
    manager = BackupManager(repo_root)
    
    print("\n🔍 Available backups:")
    backups = manager.list_backups()
    if backups:
        for backup in backups:
            print(f"   📦 {backup['name']} - {backup['created_at']} ({backup['files_count']} items)")
    else:
        print("   No backups found")
    
    print("\n" + "="*70)
    answer = input("\nCreate new backup? (yes/no): ")
    if answer.lower() == 'yes':
        backup_name, backup_path = manager.create_backup()
        print(f"\n✅ Backup created: {backup_name}")
