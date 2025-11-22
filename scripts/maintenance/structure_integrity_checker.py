"""
Repository Structure Integrity Checker
Prevents disorganization by validating structure on every commit

Part of MayAssistant Repository Restructure Safety System
"""

import os
import sys
from pathlib import Path


class StructureIntegrityChecker:
    """Validates repository structure against rules"""
    
    def __init__(self, repo_root):
        self.repo_root = Path(repo_root)
        self.violations = []
        
        # Define allowed root-level items
        self.allowed_root_files = {
            ".gitignore",
            ".env",
            ".env.example",
            "README.md",
            "CONTRIBUTING.md",
            "LICENSE",
            "package.json",
            "package-lock.json",
            "host.json",
            "local.settings.json",
            "index.js"
        }
        
        self.allowed_root_dirs = {
            ".git",
            ".github",
            ".cursor",
            "node_modules",
            "backups",
            "_archive",
            "_reports",
            "backend",  # Until migration complete
            "services",
            "omega-frontend",
            "docs",
            "infrastructure",
            "packs",
            "cursor",
            "diagnostics",
            "scripts",
            "tests"
        }
    
    def check(self):
        """Run all integrity checks"""
        print("🔍 Checking repository structure integrity...")
        
        self.check_root_level()
        self.check_duplicate_tests()
        self.check_legacy_in_root()
        self.check_reports_in_root()
        self.check_scripts_in_root()
        
        if self.violations:
            print("\n❌ STRUCTURE VIOLATIONS FOUND:")
            print("-"*70)
            for violation in self.violations:
                print(f"   • {violation}")
            print("-"*70)
            print("\n💡 Fix suggestions:")
            print("   - Run: python scripts/maintenance/restructure_repo.py --dry-run")
            print("   - Or move files to appropriate directories:")
            print("     • Reports → _reports/")
            print("     • Scripts → scripts/")
            print("     • Legacy code → _archive/")
            return False
        
        print("✅ Repository structure is clean!")
        return True
    
    def check_root_level(self):
        """Check for unauthorized files at root level"""
        root_items = set(os.listdir(self.repo_root))
        
        for item in root_items:
            item_path = self.repo_root / item
            
            # Check files
            if item_path.is_file():
                if item not in self.allowed_root_files:
                    # Special case for .md files - suggest reports directory
                    if item.endswith('.md'):
                        self.violations.append(
                            f"Documentation at root: {item} → should be in _reports/"
                        )
                    elif item.endswith(('.py', '.sh', '.ps1', '.bat')):
                        self.violations.append(
                            f"Script at root: {item} → should be in scripts/"
                        )
                    else:
                        self.violations.append(
                            f"Unauthorized file at root: {item}"
                        )
            
            # Check directories
            elif item_path.is_dir():
                if item not in self.allowed_root_dirs:
                    self.violations.append(
                        f"Unauthorized directory at root: {item}"
                    )
    
    def check_duplicate_tests(self):
        """Check for duplicate test directories"""
        backend_tests = self.repo_root / "backend" / "tests"
        tests_backend = self.repo_root / "tests" / "backend"
        
        if backend_tests.exists() and tests_backend.exists():
            self.violations.append(
                "Duplicate test directories: backend/tests/ AND tests/backend/"
            )
    
    def check_legacy_in_root(self):
        """Check for legacy code directories at root"""
        legacy_dirs = [
            "api", "dashboard", "dev-portal", "deploy_tmp",
            "functions", "legacy_v3_functions", "shared"
        ]
        
        for dir_name in legacy_dirs:
            dir_path = self.repo_root / dir_name
            if dir_path.exists():
                self.violations.append(
                    f"Legacy code at root: {dir_name}/ → should be in _archive/"
                )
    
    def check_reports_in_root(self):
        """Check for report files at root"""
        report_patterns = [
            "PHASE_", "REPORT", "HANDOFF", "ANALYSIS", 
            "CHECKLIST", "GUIDE", "SUMMARY"
        ]
        
        for item in os.listdir(self.repo_root):
            if item.endswith('.md'):
                item_upper = item.upper()
                if any(pattern in item_upper for pattern in report_patterns):
                    if item not in ["README.md", "CONTRIBUTING.md"]:
                        self.violations.append(
                            f"Report at root: {item} → should be in _reports/"
                        )
    
    def check_scripts_in_root(self):
        """Check for script files at root"""
        script_extensions = ['.py', '.sh', '.ps1', '.bat', '.cmd']
        
        for item in os.listdir(self.repo_root):
            if any(item.endswith(ext) for ext in script_extensions):
                # Exclude some allowed scripts
                if item not in ['scan_frontend.py', 'deep_scan.py']:
                    self.violations.append(
                        f"Script at root: {item} → should be in scripts/"
                    )


def main():
    """Main entry point"""
    repo_root = Path(os.getcwd())
    
    checker = StructureIntegrityChecker(repo_root)
    passed = checker.check()
    
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
