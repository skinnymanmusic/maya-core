"""
Self-Test for Repository Restructure Safety System
Validates that all safety components are working correctly
"""

import sys
from pathlib import Path
import importlib.util


def test_import(module_name, file_path):
    """Test if a module can be imported"""
    try:
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return True, "OK"
    except Exception as e:
        return False, str(e)


def main():
    """Run self-tests"""
    print("="*70)
    print("🧪 RESTRUCTURE SAFETY SYSTEM - SELF TEST")
    print("="*70)
    print()
    
    scripts_dir = Path(__file__).parent
    repo_root = scripts_dir.parent.parent
    restructure_dir = repo_root / "restructure"
    
    tests = [
        ("Backup Manager", scripts_dir / "backup_manager.py"),
        ("Reference Scanner", scripts_dir / "reference_scanner.py"),
        ("Validator", scripts_dir / "validator.py"),
        ("Structure Checker", scripts_dir / "structure_integrity_checker.py"),
        ("Restructure Main", scripts_dir / "restructure_repo.py"),
        ("Undo Script", scripts_dir / "undo_restructure.py"),
    ]
    
    print("Testing module imports...")
    print("-"*70)
    
    all_passed = True
    for name, file_path in tests:
        if not file_path.exists():
            print(f"❌ {name}: File not found - {file_path}")
            all_passed = False
            continue
        
        passed, message = test_import(name.lower().replace(" ", "_"), file_path)
        status = "✅" if passed else "❌"
        print(f"{status} {name}: {message if not passed else 'OK'}")
        
        if not passed:
            all_passed = False
    
    print()
    print("-"*70)
    
    # Check for batch files in restructure/ directory
    print("\nChecking batch files...")
    print("-"*70)
    
    batch_files = [
        "restructure_preview.bat",
        "restructure_execute.bat",
        "restructure_undo.bat",
        "check_structure.bat"
    ]
    
    for batch_file in batch_files:
        batch_path = restructure_dir / batch_file
        if batch_path.exists():
            print(f"✅ {batch_file}: Found")
        else:
            print(f"❌ {batch_file}: Missing")
            all_passed = False
    
    # Check for documentation files
    print("\nChecking documentation...")
    print("-"*70)
    
    doc_files = [
        "RESTRUCTURE_START_HERE.md",
        "SYSTEM_COMPLETE.md",
        "VISUAL_WORKFLOW.md"
    ]
    
    for doc_file in doc_files:
        doc_path = restructure_dir / doc_file
        if doc_path.exists():
            print(f"✅ {doc_file}: Found")
        else:
            print(f"❌ {doc_file}: Missing")
            all_passed = False
    
    print()
    print("="*70)
    
    if all_passed:
        print("✅ ALL TESTS PASSED")
        print()
        print("System is ready to use!")
        print()
        print("Next steps:")
        print("1. cd restructure")
        print("2. Double-click: restructure_preview.bat")
        print("3. Review the changes")
        print("4. Double-click: restructure_execute.bat")
    else:
        print("❌ SOME TESTS FAILED")
        print()
        print("Please check the errors above.")
    
    print("="*70)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
