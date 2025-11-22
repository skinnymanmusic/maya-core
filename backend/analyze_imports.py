#!/usr/bin/env python3
"""
MAYA Backend Import & Dependency Analyzer
Scans all Python files for imports and builds dependency map
"""
import os
import ast
import json
from pathlib import Path
from typing import Dict, Set, List, Tuple
from collections import defaultdict

def extract_imports(file_path: str) -> Dict[str, any]:
    """Extract all imports from a Python file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            tree = ast.parse(content, filename=file_path)

        imports = {
            'from_imports': [],
            'direct_imports': [],
            'app_imports': [],
            'external_imports': [],
            'symbols': []
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for alias in node.names:
                    import_str = f"from {module} import {alias.name}"
                    imports['from_imports'].append(import_str)
                    imports['symbols'].append(alias.name)

                    if module.startswith('app.') or module == 'app':
                        imports['app_imports'].append({
                            'module': module,
                            'symbol': alias.name,
                            'full': import_str
                        })
                    else:
                        imports['external_imports'].append(module.split('.')[0])

            elif isinstance(node, ast.Import):
                for alias in node.names:
                    import_str = f"import {alias.name}"
                    imports['direct_imports'].append(import_str)

                    if alias.name.startswith('app.') or alias.name == 'app':
                        imports['app_imports'].append({
                            'module': alias.name,
                            'symbol': None,
                            'full': import_str
                        })
                    else:
                        imports['external_imports'].append(alias.name.split('.')[0])

        return imports
    except Exception as e:
        return {'error': str(e), 'file': file_path}

def check_symbol_exists(module_file: Path, symbol: str) -> bool:
    """Check if a symbol exists in a module"""
    try:
        with open(module_file, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == symbol:
                return True
            elif isinstance(node, ast.ClassDef) and node.name == symbol:
                return True
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == symbol:
                        return True
        return False
    except:
        return False

# Main analysis
app_root = Path('app')
all_files = {}
all_imports = {}
external_deps = defaultdict(int)
import_issues = []

print("=" * 80)
print("MAYA BACKEND FULL IMPORT ANALYSIS")
print("=" * 80)

# Step 1: Map all modules
print("\n[1/4] Mapping all Python modules...")
for py_file in sorted(app_root.rglob('*.py')):
    rel_path = str(py_file)
    module_path = rel_path.replace(os.sep, '.').replace('.py', '')
    all_files[module_path] = py_file

print(f"   Found {len(all_files)} Python modules")

# Step 2: Extract all imports
print("\n[2/4] Extracting imports from all files...")
for module_path, file_path in all_files.items():
    imports = extract_imports(str(file_path))
    all_imports[module_path] = imports

    if 'error' in imports:
        import_issues.append({
            'type': 'parse_error',
            'file': module_path,
            'error': imports['error']
        })
    else:
        # Track external dependencies
        for ext_dep in imports.get('external_imports', []):
            if ext_dep and ext_dep != 'app':
                external_deps[ext_dep] += 1

print(f"   Analyzed {len(all_imports)} files")
print(f"   Found {len(external_deps)} unique external dependencies")

# Step 3: Verify app.* imports
print("\n[3/4] Verifying all app.* imports...")
verified_count = 0
missing_count = 0

for module_path, imports in all_imports.items():
    if 'error' in imports:
        continue

    for app_import in imports.get('app_imports', []):
        verified_count += 1
        imported_module = app_import['module']
        imported_symbol = app_import['symbol']

        # Convert module path to file path
        if imported_module == 'app':
            target_file = app_root / '__init__.py'
        else:
            module_parts = imported_module.split('.')
            if module_parts[0] == 'app':
                module_parts = module_parts[1:]
            target_file = app_root / Path(*module_parts[:-1]) / f"{module_parts[-1]}.py"

            # Also try as package
            if not target_file.exists():
                target_file = app_root / Path(*module_parts) / '__init__.py'

        # Check if module exists
        if not target_file.exists():
            import_issues.append({
                'type': 'missing_module',
                'file': module_path,
                'import': app_import['full'],
                'target_module': imported_module,
                'expected_path': str(target_file)
            })
            missing_count += 1
            continue

        # Check if symbol exists (if importing specific symbol)
        if imported_symbol and imported_symbol != '*':
            if not check_symbol_exists(target_file, imported_symbol):
                import_issues.append({
                    'type': 'missing_symbol',
                    'file': module_path,
                    'import': app_import['full'],
                    'target_module': imported_module,
                    'symbol': imported_symbol,
                    'target_file': str(target_file)
                })
                missing_count += 1

print(f"   Verified {verified_count} app.* imports")
print(f"   Found {missing_count} potential issues")

# Step 4: Generate reports
print("\n[4/4] Generating analysis reports...")

# Report: Module Structure
with open('docs/REPORT_FULL_DEPENDENCY_MAP.md', 'w', encoding='utf-8') as f:
    f.write("# Maya Backend - Full Dependency Map\n\n")
    f.write("Generated by automated import analyzer\n\n")
    f.write(f"**Total Modules:** {len(all_files)}\n\n")

    f.write("## Module Structure\n\n")
    f.write("```\n")
    for module in sorted(all_files.keys()):
        indent = "  " * (module.count('.') - 1)
        name = module.split('.')[-1]
        f.write(f"{indent}- {name}\n")
    f.write("```\n\n")

    f.write("## External Dependencies Used\n\n")
    f.write("| Dependency | Import Count |\n")
    f.write("|------------|-------------|\n")
    for dep, count in sorted(external_deps.items(), key=lambda x: -x[1]):
        f.write(f"| {dep} | {count} |\n")

# Report: Import Issues
with open('docs/REPORT_IMPORT_ISSUES.md', 'w', encoding='utf-8') as f:
    f.write("# Maya Backend - Import Issues Report\n\n")
    f.write(f"**Total Issues Found:** {len(import_issues)}\n\n")

    if not import_issues:
        f.write("✅ **No import issues found!**\n")
    else:
        # Group by type
        by_type = defaultdict(list)
        for issue in import_issues:
            by_type[issue['type']].append(issue)

        for issue_type, issues in by_type.items():
            f.write(f"## {issue_type.replace('_', ' ').title()} ({len(issues)})\n\n")
            for issue in issues:
                f.write(f"### {issue['file']}\n")
                f.write(f"- **Import:** `{issue.get('import', 'N/A')}`\n")
                if 'symbol' in issue:
                    f.write(f"- **Missing Symbol:** `{issue['symbol']}`\n")
                if 'target_file' in issue:
                    f.write(f"- **Target File:** `{issue['target_file']}`\n")
                if 'error' in issue:
                    f.write(f"- **Error:** {issue['error']}\n")
                f.write("\n")

print("\n✅ Analysis complete!")
print("\nReports generated:")
print("  - docs/REPORT_FULL_DEPENDENCY_MAP.md")
print("  - docs/REPORT_IMPORT_ISSUES.md")
print(f"\nSummary:")
print(f"  Modules: {len(all_files)}")
print(f"  External deps: {len(external_deps)}")
print(f"  Import issues: {len(import_issues)}")
