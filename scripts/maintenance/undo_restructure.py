"""
Repository Restructure UNDO Script
Part of MayAssistant Repository Restructure Safety System

This script safely rolls back a repository restructure by:
- Restoring from timestamped backup
- Verifying backup integrity
- Complete restoration of all files
- Validation of restored state
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime
import json

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from backup_manager import BackupManager
from validator import RestructureValidator


class RestructureUndo:
    """Handles safe rollback of repository restructure"""
    
    def __init__(self, repo_root):
        self.repo_root = Path(repo_root)
        self.backup_manager = BackupManager(self.repo_root)
        self.validator = RestructureValidator(self.repo_root)
    
    def list_available_backups(self):
        """List all available backups"""
        backups = self.backup_manager.list_backups()
        
        if not backups:
            print("❌ No backups found!")
            return []
        
        print("\n📦 Available Backups:")
        print("-"*70)
        for i, backup in enumerate(backups, 1):
            print(f"{i}. {backup['name']}")
            print(f"   Created: {backup['created_at']}")
            print(f"   Files: {backup['files_count']}")
            print()
        
        return backups
    
    def undo(self, backup_name=None):
        """Undo restructure by restoring from backup"""
        print("="*70)
        print("↩️  MAYA REPOSITORY RESTRUCTURE UNDO")
        print("="*70)
        print(f"Repository: {self.repo_root}")
        print("="*70)
        
        try:
            # Step 1: Select backup
            print("\n📦 STEP 1: Select Backup")
            print("-"*70)
            
            if backup_name:
                backup_path = self.backup_manager.backup_dir / backup_name
                if not backup_path.exists():
                    print(f"❌ Backup not found: {backup_name}")
                    return False
                print(f"Using specified backup: {backup_name}")
            else:
                backups = self.list_available_backups()
                if not backups:
                    return False
                
                choice = input("Select backup number (or 'q' to quit): ").strip()
                if choice.lower() == 'q':
                    print("Undo cancelled")
                    return False
                
                try:
                    idx = int(choice) - 1
                    if idx < 0 or idx >= len(backups):
                        print("❌ Invalid backup number")
                        return False
                    backup_name = backups[idx]['name']
                    backup_path = backups[idx]['path']
                except ValueError:
                    print("❌ Invalid input")
                    return False
            
            # Step 2: Verify backup
            print("\n🔍 STEP 2: Verify Backup Integrity")
            print("-"*70)
            valid, message = self.backup_manager.verify_backup(backup_name)
            if not valid:
                print(f"❌ Backup verification failed: {message}")
                return False
            print(f"✅ {message}")
            
            # Step 3: Confirm restore
            print("\n⚠️  STEP 3: Confirm Restore")
            print("-"*70)
            print("⚠️  WARNING: This will:")
            print("   - Delete newly created directories (_archive, _reports, services)")
            print("   - Restore all files from backup")
            print("   - Overwrite any changes made after backup")
            print()
            confirm = input("Type 'RESTORE' to proceed: ").strip()
            
            if confirm != 'RESTORE':
                print("Undo cancelled")
                return False
            
            # Step 4: Clean new structure
            print("\n🧹 STEP 4: Cleaning New Structure")
            print("-"*70)
            self.clean_new_structure()
            
            # Step 5: Restore from backup
            print("\n📥 STEP 5: Restoring from Backup")
            print("-"*70)
            self.restore_backup(backup_path)
            
            # Step 6: Validate restoration
            print("\n✅ STEP 6: Validate Restoration")
            print("-"*70)
            if not self.validate_restore():
                print("⚠️  Warning: Post-restore validation had issues")
                print("   Manual verification recommended")
            
            print("\n" + "="*70)
            print("✅ RESTORE COMPLETE!")
            print("="*70)
            print("\n✓ Repository restored to pre-restructure state")
            print(f"✓ Backup preserved: {backup_name}")
            
            return True
            
        except Exception as e:
            print(f"\n❌ ERROR during restore: {e}")
            print("\n⚠️  Repository may be in inconsistent state!")
            print("   Please check manually or contact support")
            return False
    
    def clean_new_structure(self):
        """Remove directories created by restructure"""
        new_dirs = ["_archive", "_reports", "services"]
        
        for dir_name in new_dirs:
            dir_path = self.repo_root / dir_name
            if dir_path.exists():
                print(f"   🗑️  Removing: {dir_name}")
                try:
                    shutil.rmtree(dir_path)
                    print(f"      ✓ Removed")
                except Exception as e:
                    print(f"      ✗ Error: {e}")
    
    def restore_backup(self, backup_path):
        """Restore all files from backup"""
        print(f"   📂 Restoring from: {backup_path.name}")
        
        # Get list of items in backup
        items = [
            item for item in backup_path.iterdir() 
            if item.name != "backup_metadata.json"
        ]
        
        restored = 0
        for item in items:
            dst = self.repo_root / item.name
            
            try:
                if item.is_dir():
                    # If destination exists, remove it first
                    if dst.exists():
                        shutil.rmtree(dst)
                    shutil.copytree(item, dst)
                    print(f"      ✓ {item.name}/")
                else:
                    shutil.copy2(item, dst)
                    print(f"      ✓ {item.name}")
                restored += 1
            except Exception as e:
                print(f"      ✗ {item.name}: {e}")
        
        print(f"\n   ✅ Restored {restored} items")
    
    def validate_restore(self):
        """Validate restored repository"""
        # Run basic checks
        required_dirs = ["backend", "docs", "infrastructure"]
        missing = []
        
        for dir_name in required_dirs:
            if not (self.repo_root / dir_name).exists():
                missing.append(dir_name)
        
        if missing:
            print(f"   ⚠️  Missing directories: {', '.join(missing)}")
            return False
        
        print(f"   ✅ All required directories present")
        
        # Check for leftover new structure
        new_structure = ["_archive", "_reports", "services"]
        leftover = [d for d in new_structure if (self.repo_root / d).exists()]
        
        if leftover:
            print(f"   ⚠️  Leftover directories: {', '.join(leftover)}")
            return False
        
        return True


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Undo Maya repository restructure"
    )
    parser.add_argument(
        "backup_name",
        nargs='?',
        help="Specific backup to restore (optional - will prompt if not provided)"
    )
    parser.add_argument(
        "--repo-root",
        default=os.getcwd(),
        help="Repository root directory (default: current directory)"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available backups and exit"
    )
    
    args = parser.parse_args()
    
    repo_root = Path(args.repo_root).resolve()
    
    if not (repo_root / ".git").exists():
        print(f"❌ Error: {repo_root} is not a git repository")
        sys.exit(1)
    
    undo = RestructureUndo(repo_root)
    
    if args.list:
        undo.list_available_backups()
        sys.exit(0)
    
    success = undo.undo(args.backup_name)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
