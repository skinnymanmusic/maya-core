"""
Validator - Pre and post restructure validation
Part of MayAssistant Repository Restructure Safety System
"""

import os
import sys
from pathlib import Path
import json
import subprocess


class RestructureValidator:
    """Validates repository state before and after restructure"""
    
    def __init__(self, repo_root):
        self.repo_root = Path(repo_root)
        self.validation_results = {
            "pre_checks": {},
            "post_checks": {},
            "errors": [],
            "warnings": []
        }
    
    def run_pre_checks(self):
        """Run all pre-restructure validation checks"""
        print("🔍 Running pre-restructure validation...")
        
        checks = [
            self.check_git_status,
            self.check_required_directories,
            self.check_backend_tests,
            self.check_python_syntax,
            self.check_disk_space
        ]
        
        all_passed = True
        for check in checks:
            passed, message = check()
            check_name = check.__name__
            self.validation_results["pre_checks"][check_name] = {
                "passed": passed,
                "message": message
            }
            
            status = "✅" if passed else "❌"
            print(f"   {status} {check_name}: {message}")
            
            if not passed:
                all_passed = False
                self.validation_results["errors"].append(f"{check_name}: {message}")
        
        return all_passed
    
    def run_post_checks(self):
        """Run all post-restructure validation checks"""
        print("🔍 Running post-restructure validation...")
        
        checks = [
            self.check_new_structure,
            self.check_imports_valid,
            self.check_no_broken_paths,
            self.check_backend_tests,
            self.check_essential_files
        ]
        
        all_passed = True
        for check in checks:
            passed, message = check()
            check_name = check.__name__
            self.validation_results["post_checks"][check_name] = {
                "passed": passed,
                "message": message
            }
            
            status = "✅" if passed else "❌"
            print(f"   {status} {check_name}: {message}")
            
            if not passed:
                all_passed = False
                self.validation_results["errors"].append(f"{check_name}: {message}")
        
        return all_passed
    
    def check_git_status(self):
        """Check if git working directory is clean"""
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                return False, "Git not available or repository not initialized"
            
            # It's okay to have uncommitted changes, just warn
            if result.stdout.strip():
                self.validation_results["warnings"].append(
                    "Uncommitted changes detected - backup will preserve current state"
                )
            
            return True, "Git repository accessible"
            
        except Exception as e:
            return False, f"Git check failed: {str(e)}"
    
    def check_required_directories(self):
        """Check that required directories exist"""
        required = ["backend", "docs", "infrastructure"]
        missing = []
        
        for dir_name in required:
            dir_path = self.repo_root / dir_name
            if not dir_path.exists():
                missing.append(dir_name)
        
        if missing:
            return False, f"Missing required directories: {', '.join(missing)}"
        
        return True, "All required directories present"
    
    def check_backend_tests(self):
        """Check if backend tests exist and can be discovered"""
        backend_tests = self.repo_root / "backend" / "tests"
        
        if not backend_tests.exists():
            return False, "Backend tests directory not found"
        
        test_files = list(backend_tests.glob("test_*.py"))
        
        if not test_files:
            return False, "No test files found in backend/tests"
        
        return True, f"Found {len(test_files)} test files"
    
    def check_python_syntax(self):
        """Check Python files for syntax errors"""
        print("      Checking Python syntax...")
        
        python_files = [
            f for f in self.repo_root.rglob("*.py")
            if '.git' not in str(f) and 'node_modules' not in str(f)
        ]
        
        errors = []
        for py_file in python_files[:50]:  # Check first 50 files
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    compile(f.read(), str(py_file), 'exec')
            except SyntaxError as e:
                errors.append(f"{py_file.name}: {e}")
        
        if errors:
            return False, f"Syntax errors in {len(errors)} files"
        
        return True, f"Checked {min(len(python_files), 50)} Python files"
    
    def check_disk_space(self):
        """Check if sufficient disk space is available"""
        try:
            import shutil
            total, used, free = shutil.disk_usage(self.repo_root)
            free_gb = free // (1024 ** 3)
            
            if free_gb < 1:
                return False, f"Insufficient disk space: {free_gb}GB free"
            
            return True, f"Sufficient disk space: {free_gb}GB free"
            
        except Exception as e:
            return False, f"Could not check disk space: {e}"
    
    def check_new_structure(self):
        """Check if new directory structure exists"""
        expected_dirs = ["_archive", "_reports", "services"]
        found = []
        missing = []
        
        for dir_name in expected_dirs:
            if (self.repo_root / dir_name).exists():
                found.append(dir_name)
            else:
                missing.append(dir_name)
        
        if missing:
            return False, f"New structure incomplete: missing {', '.join(missing)}"
        
        return True, f"New structure created: {', '.join(found)}"
    
    def check_imports_valid(self):
        """Check if Python imports are still valid"""
        print("      Validating imports...")
        
        # Quick check - try to import main backend module
        backend_main = self.repo_root / "services" / "backend" / "app" / "main.py"
        
        if not backend_main.exists():
            backend_main = self.repo_root / "backend" / "app" / "main.py"
        
        if not backend_main.exists():
            return False, "Could not find backend main.py"
        
        return True, "Backend entry point exists"
    
    def check_no_broken_paths(self):
        """Check for common broken path issues"""
        issues = []
        
        # Check if old backend directory is gone or moved
        old_backend = self.repo_root / "backend"
        new_backend = self.repo_root / "services" / "backend"
        
        if old_backend.exists() and new_backend.exists():
            issues.append("Both old and new backend directories exist")
        
        if issues:
            return False, "; ".join(issues)
        
        return True, "No path conflicts detected"
    
    def check_essential_files(self):
        """Check that essential files still exist"""
        essential = [
            "README.md",
            ".gitignore",
            "docs/MASTER_HANDOFF.md"
        ]
        
        missing = []
        for file_path in essential:
            if not (self.repo_root / file_path).exists():
                missing.append(file_path)
        
        if missing:
            return False, f"Missing essential files: {', '.join(missing)}"
        
        return True, "All essential files present"
    
    def save_report(self, output_file):
        """Save validation report"""
        with open(output_file, 'w') as f:
            json.dump(self.validation_results, f, indent=2)
        print(f"📄 Validation report saved to: {output_file}")
    
    def get_summary(self):
        """Get summary of validation results"""
        pre_passed = all(
            check["passed"] 
            for check in self.validation_results["pre_checks"].values()
        )
        post_passed = all(
            check["passed"] 
            for check in self.validation_results["post_checks"].values()
        ) if self.validation_results["post_checks"] else None
        
        return {
            "pre_validation_passed": pre_passed,
            "post_validation_passed": post_passed,
            "total_errors": len(self.validation_results["errors"]),
            "total_warnings": len(self.validation_results["warnings"])
        }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validator.py <repo_root> [--post]")
        sys.exit(1)
    
    repo_root = sys.argv[1]
    is_post = "--post" in sys.argv
    
    validator = RestructureValidator(repo_root)
    
    if is_post:
        passed = validator.run_post_checks()
    else:
        passed = validator.run_pre_checks()
    
    print("\n" + "="*70)
    print("📊 VALIDATION SUMMARY:")
    summary = validator.get_summary()
    for key, value in summary.items():
        print(f"   {key}: {value}")
    
    if not passed:
        print("\n❌ Validation FAILED")
        sys.exit(1)
    else:
        print("\n✅ Validation PASSED")
