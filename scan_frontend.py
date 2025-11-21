#!/usr/bin/env python3
"""
Comprehensive Frontend Scan
Analyzes omega-frontend to determine what exists vs what's missing
"""

import os
import json
from pathlib import Path

def scan_directory(path, prefix=""):
    """Recursively scan directory and categorize files"""
    results = {
        "empty_dirs": [],
        "empty_files": [],
        "stub_files": [],  # Files with only types/TODOs
        "complete_files": [],  # Files with actual implementation
        "missing_expected": []
    }
    
    try:
        items = list(Path(path).iterdir())
    except PermissionError:
        return results
    
    for item in sorted(items):
        if item.name in ['.next', 'node_modules', '.git', '__pycache__']:
            continue
            
        rel_path = f"{prefix}/{item.name}" if prefix else item.name
        
        if item.is_dir():
            # Check if directory is empty
            try:
                if not any(item.iterdir()):
                    results["empty_dirs"].append(rel_path)
                else:
                    # Recursively scan subdirectory
                    sub_results = scan_directory(item, rel_path)
                    for key in results:
                        results[key].extend(sub_results[key])
            except PermissionError:
                pass
                
        elif item.is_file():
            # Check file size and content
            size = item.stat().st_size
            
            if size == 0:
                results["empty_files"].append(rel_path)
            else:
                # Read file to check if it's a stub
                try:
                    with open(item, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Check if it's a stub (mostly TODOs, types, or very short)
                    if 'TODO' in content and len(content) < 500:
                        results["stub_files"].append(rel_path)
                    else:
                        results["complete_files"].append(rel_path)
                except:
                    results["complete_files"].append(rel_path)
    
    return results

def check_expected_pages():
    """Check for expected Next.js pages"""
    expected_pages = [
        "src/app/(app)/dashboard/page.tsx",
        "src/app/(app)/agents/page.tsx",
        "src/app/(app)/automations/page.tsx",
        "src/app/(app)/messages/page.tsx",
        "src/app/(app)/clients/page.tsx",
        "src/app/(app)/events/page.tsx",
        "src/app/(app)/payments/page.tsx",
        "src/app/(app)/files/page.tsx",
        "src/app/(app)/settings/page.tsx",
        "src/app/(app)/integrations/page.tsx",
        "src/app/(app)/developer/page.tsx"
    ]
    
    missing = []
    for page in expected_pages:
        if not Path(f"omega-frontend/{page}").exists():
            missing.append(page)
    
    return missing

def main():
    print("=" * 80)
    print("OMEGA FRONTEND COMPREHENSIVE SCAN")
    print("=" * 80)
    print()
    
    frontend_path = Path("omega-frontend")
    
    if not frontend_path.exists():
        print("❌ ERROR: omega-frontend directory not found!")
        return
    
    print("📁 Scanning omega-frontend directory...")
    print()
    
    # Check package.json
    package_json = frontend_path / "package.json"
    if package_json.exists():
        with open(package_json) as f:
            pkg = json.load(f)
        print("✅ Package.json exists")
        print(f"   Next.js: {pkg['dependencies'].get('next', 'N/A')}")
        print(f"   Clerk: {pkg['dependencies'].get('@clerk/nextjs', 'N/A')}")
        print(f"   React: {pkg['dependencies'].get('react', 'N/A')}")
        print()
    
    # Scan all files
    results = scan_directory(frontend_path)
    
    print("📊 SCAN RESULTS")
    print("=" * 80)
    print()
    
    # Empty directories
    print(f"📂 Empty Directories ({len(results['empty_dirs'])})")
    if results['empty_dirs']:
        for d in results['empty_dirs'][:10]:  # Show first 10
            print(f"   ❌ {d}")
        if len(results['empty_dirs']) > 10:
            print(f"   ... and {len(results['empty_dirs']) - 10} more")
    else:
        print("   ✅ No empty directories")
    print()
    
    # Empty files
    print(f"📄 Empty Files ({len(results['empty_files'])})")
    if results['empty_files']:
        for f in results['empty_files'][:10]:
            print(f"   ❌ {f}")
        if len(results['empty_files']) > 10:
            print(f"   ... and {len(results['empty_files']) - 10} more")
    else:
        print("   ✅ No empty files")
    print()
    
    # Stub files
    print(f"📝 Stub Files (TODOs, types only) ({len(results['stub_files'])})")
    if results['stub_files']:
        for f in results['stub_files']:
            print(f"   ⚠️  {f}")
    else:
        print("   ✅ No stub files")
    print()
    
    # Complete files
    print(f"✅ Complete Files ({len(results['complete_files'])})")
    if results['complete_files']:
        print("   Key files found:")
        important = [f for f in results['complete_files'] 
                    if any(x in f for x in ['layout', 'page', 'component', 'service'])]
        for f in important[:15]:
            print(f"   ✓ {f}")
        if len(important) > 15:
            print(f"   ... and {len(important) - 15} more")
    print()
    
    # Missing expected pages
    missing_pages = check_expected_pages()
    print(f"🔍 Expected Pages Status")
    print(f"   Missing: {len(missing_pages)}/11 pages")
    if missing_pages:
        for page in missing_pages:
            print(f"   ❌ {page}")
    print()
    
    # Summary
    print("=" * 80)
    print("📋 SUMMARY")
    print("=" * 80)
    total_empty = len(results['empty_dirs']) + len(results['empty_files'])
    total_stub = len(results['stub_files'])
    total_complete = len(results['complete_files'])
    total_files = total_empty + total_stub + total_complete
    
    print(f"   Total items scanned: {total_files}")
    print(f"   ✅ Complete: {total_complete} ({total_complete/total_files*100:.1f}%)")
    print(f"   ⚠️  Stubs: {total_stub} ({total_stub/total_files*100:.1f}%)")
    print(f"   ❌ Empty: {total_empty} ({total_empty/total_files*100:.1f}%)")
    print()
    
    # Verdict
    print("🎯 VERDICT:")
    if len(missing_pages) > 8:
        print("   ❌ Frontend is mostly EMPTY - needs full rebuild")
        print("   📁 Directory structure exists but pages missing")
    elif len(missing_pages) > 4:
        print("   ⚠️  Frontend is PARTIALLY built - needs significant work")
        print("   📁 Some pages exist, many missing")
    else:
        print("   ✅ Frontend is mostly COMPLETE - needs polish")
        print("   📁 Most pages exist, minor gaps")
    print()

if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    main()
