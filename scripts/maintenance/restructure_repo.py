"""
Repository Restructure Orchestrator - Main Script
Part of MayAssistant Repository Restructure Safety System

This script safely restructures the maya-ai repository with:
- Complete backup before any changes
- Pre-flight validation
- Transaction-based moves
- Automatic reference updates
- Post-move validation
- One-command rollback capability
"""

import os
import sys
import shutil
import json
from pathlib import Path
from datetime import datetime
import re

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from backup_manager import BackupManager
from reference_scanner import ReferenceScanner
from validator import RestructureValidator


class RepositoryRestructure:
    """Orchestrates safe repository restructuring"""
    
    def __init__(self, repo_root, dry_run=False):
        self.repo_root = Path(repo_root)
        self.dry_run = dry_run
        self.backup_manager = BackupManager(self.repo_root)
        self.validator = RestructureValidator(self.repo_root)
        self.scanner = ReferenceScanner(self.repo_root)
        
        self.moves = []
        self.updates = []
        self.backup_name = None
        
        # Define restructure plan
        self.plan = {
            "archive": {
                "target": "_archive",
                "items": [
                    "api", "dashboard", "dev-portal", "deploy_tmp",
                    "functions", "legacy_v3_functions", "shared"
                ]
            },
            "reports": {
                "target": "_reports",
                "items": [
                    # Handoff documents
                    "SOLIN_HANDOFF_2025-11-21.md",
                    "MAYA_DEEP_SCAN_HANDOFF.md",
                    "CLAUDE_DESKTOP_ANALYSIS_REPORT.md",
                    
                    # Phase reports
                    "PHASE_0_COMPLETE_REPORT.md",
                    "PHASE_0_EXECUTION_PLAN.md",
                    "PHASE_0_EXECUTION_RESULTS.md",
                    "PHASE_0_SQL_PREVIEW.md",
                    "PHASE_0_VALIDATION_REPORT.md",
                    "PHASE_0-2_COMPLETE_SUMMARY.md",
                    "PHASE_0B_TEST_PLAN.md",
                    "PHASE_1_TEST_VALIDATION_REPORT.md",
                    "PHASE_2_DEPLOYMENT_READINESS_REPORT.md",
                    "PHASE_2B_DEPLOYMENT_GUIDE.md",
                    "PHASE_2B_DEPLOYMENT_READY.md",
                    
                    # Deployment docs
                    "RAILWAY_DEPLOYMENT_CHECKLIST.md",
                    "SET_ENV_VARIABLES_GUIDE.md",
                    "BACKEND_ENVIRONMENT_VARIABLES_REQUIRED.md",
                    
                    # Analysis reports
                    "FEATURE_IMPLEMENTATION_ANALYSIS.md",
                    "FULL_RECONCILIATION_REPORT.md",
                    "DOCUMENTATION_INDEX.md",
                    "GITHUB_UPLOAD_REPORT.md",
                    "QUICK_STATUS_REPORT.md",
                    "SESSION_REPORT.md",
                    "REPO_RESTRUCTURE_PLAN.md",
                    "REPOSITORY_FILE_STRUCTURE.md",
                    "MAYA_V3_IMPLEMENTATION_COMPLETE.md",
                    
                    # Archive data
                    "MAYA_DEEP_SCAN_DATA.json",
                    "directory_structure.txt",
                    "file_structure.txt",
                    
                    # Old directories
                    "PHASE_1_SUPABASE",
                    "repo_integrity_pack",
                    "repo_integrity_pack_v3",
                    "v3_integrity_pack",
                    
                    # Zip files
                    "*.zip"
                ]
            },
            "scripts": {
                "target": "scripts",
                "subdirs": {
                    "setup": [
                        "complete_setup.sh",
                        "setup_maya_rbac.sh",
                        "setup_patch_runners_unistring.py"
                    ],
                    "deployment": [
                        "migrate_to_v4.sh",
                        "fix_github_secrets.sh",
                        "set_github_secrets.ps1"
                    ],
                    "diagnostics": [
                        "scan_frontend.py",
                        "deep_scan.py",
                        "DEEP_SCAN_FOR_CLAUDE_DESKTOP.py"
                    ]
                }
            },
            "services": {
                "renames": {
                    "backend": "services/backend",
                    "nova-backend": "services/nova",
                    "eli-backend": "services/eli"
                }
            }
        }
    
    def execute(self):
        """Execute the complete restructure process"""
        print("="*70)
        print("🚀 MAYA REPOSITORY RESTRUCTURE")
        print("="*70)
        print(f"Repository: {self.repo_root}")
        print(f"Mode: {'DRY RUN' if self.dry_run else 'LIVE EXECUTION'}")
        print("="*70)
        
        try:
            # Step 1: Pre-flight validation
            print("\n📋 STEP 1: Pre-flight Validation")
            print("-"*70)
            if not self.validator.run_pre_checks():
                print("\n❌ Pre-flight validation failed!")
                return False
            
            # Step 2: Create backup
            print("\n💾 STEP 2: Creating Backup")
            print("-"*70)
            if not self.dry_run:
                self.backup_name, backup_path = self.backup_manager.create_backup()
                print(f"✅ Backup created: {self.backup_name}")
            else:
                print("   [DRY RUN] Would create backup")
            
            # Step 3: Scan references
            print("\n🔍 STEP 3: Scanning References")
            print("-"*70)
            self.scanner.scan_all()
            
            # Step 4: Execute moves
            print("\n📦 STEP 4: Executing Moves")
            print("-"*70)
            self.execute_restructure()
            
            # Step 5: Update references
            print("\n🔗 STEP 5: Updating References")
            print("-"*70)
            self.update_references()
            
            # Step 6: Post-validation
            print("\n✅ STEP 6: Post-Validation")
            print("-"*70)
            if not self.dry_run:
                if not self.validator.run_post_checks():
                    print("\n❌ Post-validation failed!")
                    print("   Run: python scripts/maintenance/undo_restructure.py")
                    return False
            else:
                print("   [DRY RUN] Would run post-validation")
            
            # Step 7: Cleanup
            print("\n🧹 STEP 7: Cleanup")
            print("-"*70)
            self.cleanup()
            
            print("\n" + "="*70)
            print("✅ RESTRUCTURE COMPLETE!")
            print("="*70)
            
            if not self.dry_run:
                print(f"\n📦 Backup: {self.backup_name}")
                print(f"↩️  Undo: python scripts/maintenance/undo_restructure.py {self.backup_name}")
            
            return True
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            print("\n🔧 Rolling back changes...")
            if not self.dry_run and self.backup_name:
                print(f"   Run: python scripts/maintenance/undo_restructure.py {self.backup_name}")
            return False
    
    def execute_restructure(self):
        """Execute all file/directory moves"""
        
        # Create target directories
        targets = ["_archive", "_reports", "services"]
        for target in targets:
            target_path = self.repo_root / target
            if not self.dry_run:
                target_path.mkdir(exist_ok=True)
            print(f"   📁 Created: {target}")
        
        # Move legacy code to archive
        print("\n   🗃️  Archiving legacy code...")
        for item in self.plan["archive"]["items"]:
            src = self.repo_root / item
            dst = self.repo_root / "_archive" / item
            if src.exists():
                self.move_item(src, dst, "Archive")
        
        # Move reports
        print("\n   📊 Moving reports...")
        for item in self.plan["reports"]["items"]:
            if "*" in item:  # Handle wildcards
                for match in self.repo_root.glob(item):
                    if match.is_file():
                        dst = self.repo_root / "_reports" / match.name
                        self.move_item(match, dst, "Report")
            else:
                src = self.repo_root / item
                if src.exists():
                    dst = self.repo_root / "_reports" / item
                    self.move_item(src, dst, "Report")
        
        # Move and organize scripts
        print("\n   📜 Organizing scripts...")
        scripts_dir = self.repo_root / "scripts"
        if not self.dry_run:
            scripts_dir.mkdir(exist_ok=True)
        
        for subdir, items in self.plan["scripts"]["subdirs"].items():
            subdir_path = scripts_dir / subdir
            if not self.dry_run:
                subdir_path.mkdir(exist_ok=True)
            
            for item in items:
                src = self.repo_root / item
                if src.exists():
                    dst = subdir_path / src.name
                    self.move_item(src, dst, "Script")
        
        # Rename/move services
        print("\n   🔧 Reorganizing services...")
        services_dir = self.repo_root / "services"
        if not self.dry_run:
            services_dir.mkdir(exist_ok=True)
        
        for old_name, new_path in self.plan["services"]["renames"].items():
            src = self.repo_root / old_name
            dst = self.repo_root / new_path
            if src.exists():
                self.move_item(src, dst, "Service")
        
        print(f"\n   ✅ Executed {len(self.moves)} moves")
    
    def move_item(self, src, dst, category):
        """Move a file or directory"""
        try:
            if self.dry_run:
                print(f"      [{category}] {src.name} → {dst}")
                self.moves.append({"src": str(src), "dst": str(dst), "category": category})
            else:
                dst.parent.mkdir(parents=True, exist_ok=True)
                if src.is_dir():
                    shutil.move(str(src), str(dst))
                else:
                    shutil.copy2(str(src), str(dst))
                    src.unlink()
                print(f"      ✓ {src.name}")
                self.moves.append({"src": str(src), "dst": str(dst), "category": category})
        except Exception as e:
            print(f"      ✗ {src.name}: {e}")
    
    def update_references(self):
        """Update all file references"""
        print("   🔗 Updating Python imports...")
        
        # Define path mappings
        mappings = {
            "from backend.": "from services.backend.",
            "import backend.": "import services.backend.",
            'backend/': 'services/backend/',
        }
        
        # Update Python files
        python_files = list(self.repo_root.rglob("*.py"))
        updated = 0
        
        for py_file in python_files:
            if '_archive' in str(py_file) or '.git' in str(py_file):
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original = content
                for old, new in mappings.items():
                    content = content.replace(old, new)
                
                if content != original and not self.dry_run:
                    with open(py_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    updated += 1
                    print(f"      ✓ {py_file.relative_to(self.repo_root)}")
                elif content != original:
                    print(f"      [DRY RUN] {py_file.relative_to(self.repo_root)}")
                    updated += 1
                    
            except Exception as e:
                print(f"      ✗ {py_file.name}: {e}")
        
        print(f"   ✅ Updated {updated} files")
    
    def cleanup(self):
        """Clean up empty directories and temporary files"""
        if self.dry_run:
            print("   [DRY RUN] Would clean up empty directories")
            return
        
        # Remove empty directories
        for root, dirs, files in os.walk(self.repo_root, topdown=False):
            for dir_name in dirs:
                dir_path = Path(root) / dir_name
                if dir_path.exists() and not any(dir_path.iterdir()):
                    try:
                        dir_path.rmdir()
                        print(f"   🗑️  Removed empty: {dir_path.relative_to(self.repo_root)}")
                    except:
                        pass


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Safely restructure Maya repository"
    )
    parser.add_argument(
        "repo_root",
        nargs='?',
        default=os.getcwd(),
        help="Repository root directory (default: current directory)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes"
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute the restructure (required for live run)"
    )
    
    args = parser.parse_args()
    
    repo_root = Path(args.repo_root).resolve()
    
    if not (repo_root / ".git").exists():
        print(f"❌ Error: {repo_root} is not a git repository")
        sys.exit(1)
    
    if not args.dry_run and not args.execute:
        print("❌ Error: Must specify either --dry-run or --execute")
        print("\nRun with --dry-run first to preview changes:")
        print(f"   python {Path(__file__).name} --dry-run")
        print("\nThen execute with:")
        print(f"   python {Path(__file__).name} --execute")
        sys.exit(1)
    
    restructure = RepositoryRestructure(repo_root, dry_run=args.dry_run)
    success = restructure.execute()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
