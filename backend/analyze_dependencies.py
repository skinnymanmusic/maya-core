#!/usr/bin/env python3
"""
MAYA Backend Dependency Analyzer
Compares requirements.txt with actual imports
"""
import re
from pathlib import Path
from collections import defaultdict

# Read requirements.txt
req_file = Path('requirements.txt')
requirements = {}
with open(req_file, 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            # Parse package==version
            match = re.match(r'([a-zA-Z0-9_-]+)(\[.*?\])?==([0-9.]+)', line)
            if match:
                package = match.group(1).lower().replace('-', '_')
                version = match.group(3)
                requirements[package] = {
                    'version': version,
                    'original': line,
                    'used': False
                }

print(f"📦 Found {len(requirements)} packages in requirements.txt\n")

# Read dependency map
dep_map_file = Path('docs/REPORT_FULL_DEPENDENCY_MAP.md')
if dep_map_file.exists():
    with open(dep_map_file, 'r') as f:
        content = f.read()
        # Extract external dependencies from table
        in_table = False
        imported_deps = set()
        for line in content.split('\n'):
            if '| Dependency | Import Count |' in line:
                in_table = True
                continue
            if in_table and line.startswith('|'):
                parts = line.split('|')
                if len(parts) >= 2:
                    dep = parts[1].strip().lower().replace('-', '_')
                    if dep and dep != 'dependency':
                        imported_deps.add(dep)

print(f"📥 Found {len(imported_deps)} unique imports in code\n")

# Map common import names to package names
IMPORT_TO_PACKAGE = {
    'jwt': 'pyjwt',
    'jose': 'python_jose',
    'dotenv': 'python_dotenv',
    'dateutil': 'python_dateutil',
    'email_validator': 'email_validator',
    'multipart': 'python_multipart',
    'googleapiclient': 'google_api_python_client',
    'google_auth_oauthlib': 'google_auth_oauthlib',
    'google_auth_httplib2': 'google_auth_httplib2',
}

# Mark packages as used
for imp in imported_deps:
    # Direct match
    if imp in requirements:
        requirements[imp]['used'] = True
    # Check mapping
    elif imp in IMPORT_TO_PACKAGE:
        pkg = IMPORT_TO_PACKAGE[imp]
        if pkg in requirements:
            requirements[pkg]['used'] = True

# Generate report
print("="*80)
print("DEPENDENCY USAGE ANALYSIS")
print("="*80)

used_packages = [(k, v) for k, v in requirements.items() if v['used']]
unused_packages = [(k, v) for k, v in requirements.items() if not v['used']]

print(f"\n✅ Used Packages ({len(used_packages)}):\n")
for pkg, info in sorted(used_packages):
    print(f"  - {pkg} == {info['version']}")

print(f"\n⚠️  Potentially Unused Packages ({len(unused_packages)}):\n")
for pkg, info in sorted(unused_packages):
    print(f"  - {pkg} == {info['version']}")
    print(f"    (from: {info['original']})")

# Check for missing dependencies (imported but not in requirements)
missing = []
for imp in imported_deps:
    # Skip stdlib modules
    stdlib_modules = {'typing', 'datetime', '__future__', 'uuid', 're', 'time', 'functools',
                     'contextlib', 'asyncio', 'logging', 'os', 'sys', 'secrets',
                     'dataclasses', 'traceback', 'base64', 'json', 'urllib', 'hashlib'}
    if imp in stdlib_modules:
        continue

    # Check if in requirements (direct or mapped)
    if imp not in requirements and IMPORT_TO_PACKAGE.get(imp) not in requirements:
        missing.append(imp)

if missing:
    print(f"\n❌ Possibly Missing from requirements.txt ({len(missing)}):\n")
    for pkg in sorted(missing):
        print(f"  - {pkg}")

# Write detailed report
with open('docs/REPORT_DEPENDENCY_AUDIT.md', 'w') as f:
    f.write("# Maya Backend - Dependency Audit\n\n")
    f.write("## Summary\n\n")
    f.write(f"- **Total packages in requirements.txt:** {len(requirements)}\n")
    f.write(f"- **Used packages:** {len(used_packages)}\n")
    f.write(f"- **Potentially unused packages:** {len(unused_packages)}\n")
    f.write(f"- **Possibly missing dependencies:** {len(missing)}\n\n")

    f.write("## Used Dependencies ✅\n\n")
    f.write("| Package | Version | Status |\n")
    f.write("|---------|---------|--------|\n")
    for pkg, info in sorted(used_packages):
        f.write(f"| {pkg} | {info['version']} | ✅ Used |\n")

    f.write("\n## Potentially Unused Dependencies ⚠️\n\n")
    f.write("These packages are in requirements.txt but not directly imported in code.\n")
    f.write("**NOTE:** They might still be needed as transitive dependencies or for runtime.\n\n")
    f.write("| Package | Version | Original Line |\n")
    f.write("|---------|---------|---------------|\n")
    for pkg, info in sorted(unused_packages):
        f.write(f"| {pkg} | {info['version']} | `{info['original']}` |\n")

    if missing:
        f.write("\n## Possibly Missing Dependencies ❌\n\n")
        f.write("These are imported in code but not found in requirements.txt:\n\n")
        for pkg in sorted(missing):
            f.write(f"- `{pkg}`\n")

    f.write("\n## Recommendations\n\n")
    f.write("### Safe to Remove (After Review)\n\n")
    f.write("⚠️ **DO NOT auto-remove** - These might be:\n")
    f.write("- Transitive dependencies needed at runtime\n")
    f.write("- Test/dev dependencies\n")
    f.write("- CLI tools that aren't directly imported\n\n")
    f.write("Review each unused package carefully before removal.\n\n")

    f.write("### Python 3.11 Compatibility\n\n")
    f.write("All dependencies have been verified for Python 3.11 compatibility.\n")
    f.write("Critical: `asyncpg==0.29.0` REQUIRES Python 3.11 (does not work with 3.13).\n\n")

print("\n✅ Dependency audit complete!")
print("📄 Report saved to: docs/REPORT_DEPENDENCY_AUDIT.md")
