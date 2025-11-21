"""
MAYA PROJECT DEEP SCANNER
=========================
Comprehensive project analysis tool for Claude Code to scan everything
and create a detailed handoff for Claude Desktop analysis.

This scanner will examine:
1. ALL code files (Python, JavaScript, TypeScript, etc.)
2. Documentation vs. implementation gaps (hallucinations)
3. Configuration drift across environments
4. Test coverage and results
5. Dependencies and their usage
6. Database schema vs. code usage
7. API endpoints documented vs. implemented
8. Frontend-backend integration points
9. TODOs, FIXMEs, and incomplete features
10. Git history and recent changes
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Any
from collections import defaultdict

class MayaDeepScanner:
    def __init__(self, root_path: str):
        self.root = Path(root_path)
        self.results = {
            'scan_time': datetime.now().isoformat(),
            'stats': {},
            'files': [],
            'hallucinations': [],
            'drift': [],
            'todos': [],
            'fixmes': [],
            'tests': {},
            'api_endpoints': {'documented': [], 'implemented': []},
            'database': {'schema_tables': [], 'code_references': []},
            'dependencies': {'documented': [], 'installed': [], 'unused': []},
            'integration_points': [],
            'config': [],
            'recent_changes': []
        }
        
        # File patterns to scan
        self.code_extensions = {'.py', '.js', '.jsx', '.ts', '.tsx', '.html', '.css', '.sql'}
        self.doc_extensions = {'.md', '.txt', '.json', '.yaml', '.yml'}
        self.config_extensions = {'.env', '.toml', '.ini', '.cfg', '.conf'}
        
        # Skip patterns
        self.skip_dirs = {'node_modules', '__pycache__', '.git', 'venv', '.venv', 'dist', 'build', '.next'}
        self.skip_files = {'.pyc', '.pyo', '.pyd', '.so', '.dll', '.dylib'}
    
    def scan_all(self):
        """Main scanning function - orchestrates all scans"""
        print("=" * 80)
        print("MAYA PROJECT DEEP SCANNER")
        print("=" * 80)
        print(f"Starting comprehensive scan at: {self.results['scan_time']}")
        print(f"Root directory: {self.root}")
        print("")
        
        # Phase 1: File inventory
        print("Phase 1: Building complete file inventory...")
        self._scan_files()
        print(f"✓ Found {len(self.results['files'])} files to analyze")
        
        # Phase 2: Code analysis
        print("\nPhase 2: Analyzing code files...")
        self._analyze_code_files()
        print(f"✓ Found {len(self.results['todos'])} TODOs")
        print(f"✓ Found {len(self.results['fixmes'])} FIXMEs")
        
        # Phase 3: API analysis
        print("\nPhase 3: Scanning API endpoints...")
        self._scan_api_endpoints()
        print(f"✓ Documented endpoints: {len(self.results['api_endpoints']['documented'])}")
        print(f"✓ Implemented endpoints: {len(self.results['api_endpoints']['implemented'])}")
        
        # Phase 4: Database analysis
        print("\nPhase 4: Analyzing database schema and usage...")
        self._scan_database()
        print(f"✓ Schema tables: {len(self.results['database']['schema_tables'])}")
        print(f"✓ Code references: {len(self.results['database']['code_references'])}")
        
        # Phase 5: Test analysis
        print("\nPhase 5: Examining test coverage...")
        self._scan_tests()
        print(f"✓ Test files: {len(self.results['tests'])}")
        
        # Phase 6: Dependency analysis
        print("\nPhase 6: Analyzing dependencies...")
        self._scan_dependencies()
        print(f"✓ Documented: {len(self.results['dependencies']['documented'])}")
        print(f"✓ Potentially unused: {len(self.results['dependencies']['unused'])}")
        
        # Phase 7: Configuration analysis
        print("\nPhase 7: Scanning configurations...")
        self._scan_config()
        print(f"✓ Config files: {len(self.results['config'])}")
        
        # Phase 8: Hallucination detection
        print("\nPhase 8: Detecting hallucinations...")
        self._detect_hallucinations()
        print(f"✓ Potential hallucinations: {len(self.results['hallucinations'])}")
        
        # Phase 9: Drift detection
        print("\nPhase 9: Detecting drift...")
        self._detect_drift()
        print(f"✓ Drift issues: {len(self.results['drift'])}")
        
        # Phase 10: Integration analysis
        print("\nPhase 10: Analyzing integration points...")
        self._scan_integrations()
        print(f"✓ Integration points: {len(self.results['integration_points'])}")
        
        # Generate report
        print("\nPhase 11: Generating comprehensive handoff...")
        self._generate_handoff()
        print("✓ Handoff complete")
        
        print("\n" + "=" * 80)
        print("SCAN COMPLETE!")
        print("=" * 80)
    
    def _scan_files(self):
        """Build complete file inventory"""
        for root, dirs, files in os.walk(self.root):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in self.skip_dirs]
            
            for file in files:
                file_path = Path(root) / file
                rel_path = file_path.relative_to(self.root)
                ext = file_path.suffix.lower()
                
                # Skip excluded files
                if ext in self.skip_files:
                    continue
                
                file_info = {
                    'path': str(rel_path),
                    'full_path': str(file_path),
                    'type': self._categorize_file(ext),
                    'size': file_path.stat().st_size if file_path.exists() else 0,
                    'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat() if file_path.exists() else None
                }
                self.results['files'].append(file_info)
    
    def _categorize_file(self, ext: str) -> str:
        """Categorize file by extension"""
        if ext in self.code_extensions:
            return 'code'
        elif ext in self.doc_extensions:
            return 'documentation'
        elif ext in self.config_extensions:
            return 'config'
        else:
            return 'other'
    
    def _analyze_code_files(self):
        """Analyze all code files for TODOs, FIXMEs, and patterns"""
        code_files = [f for f in self.results['files'] if f['type'] == 'code']
        
        for file_info in code_files:
            try:
                with open(file_info['full_path'], 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    lines = content.split('\n')
                    
                    for i, line in enumerate(lines, 1):
                        # Find TODOs
                        if 'TODO' in line.upper():
                            self.results['todos'].append({
                                'file': file_info['path'],
                                'line': i,
                                'content': line.strip()
                            })
                        
                        # Find FIXMEs
                        if 'FIXME' in line.upper() or 'BUG' in line.upper():
                            self.results['fixmes'].append({
                                'file': file_info['path'],
                                'line': i,
                                'content': line.strip()
                            })
            except Exception as e:
                print(f"  ⚠ Could not read {file_info['path']}: {e}")
    
    def _scan_api_endpoints(self):
        """Scan for API endpoints in code and documentation"""
        # Scan FastAPI routes in backend
        backend_files = [f for f in self.results['files'] if 'backend' in f['path'] and f['path'].endswith('.py')]
        
        route_patterns = [
            r'@router\.(get|post|put|delete|patch)\(["\']([^"\']+)["\']',
            r'@app\.(get|post|put|delete|patch)\(["\']([^"\']+)["\']',
        ]
        
        for file_info in backend_files:
            try:
                with open(file_info['full_path'], 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    for pattern in route_patterns:
                        matches = re.finditer(pattern, content)
                        for match in matches:
                            method = match.group(1).upper()
                            path = match.group(2)
                            self.results['api_endpoints']['implemented'].append({
                                'method': method,
                                'path': path,
                                'file': file_info['path']
                            })
            except Exception as e:
                print(f"  ⚠ Could not scan {file_info['path']}: {e}")
        
        # Scan documentation for endpoint references
        doc_files = [f for f in self.results['files'] if f['type'] == 'documentation']
        endpoint_pattern = r'(GET|POST|PUT|DELETE|PATCH)\s+(/[^\s\)]+)'
        
        for file_info in doc_files:
            try:
                with open(file_info['full_path'], 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    matches = re.finditer(endpoint_pattern, content)
                    for match in matches:
                        self.results['api_endpoints']['documented'].append({
                            'method': match.group(1),
                            'path': match.group(2),
                            'file': file_info['path']
                        })
            except Exception as e:
                print(f"  ⚠ Could not scan {file_info['path']}: {e}")
    
    def _scan_database(self):
        """Analyze database schema and code references"""
        # Find schema files
        schema_files = [f for f in self.results['files'] 
                       if 'schema' in f['path'].lower() or 'migration' in f['path'].lower()]
        
        table_pattern = r'CREATE TABLE\s+(\w+)'
        model_pattern = r'class\s+(\w+)\s*\([^)]*Base[^)]*\)'
        
        for file_info in schema_files:
            try:
                with open(file_info['full_path'], 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    # Find table definitions
                    tables = re.findall(table_pattern, content, re.IGNORECASE)
                    for table in tables:
                        self.results['database']['schema_tables'].append({
                            'name': table,
                            'file': file_info['path']
                        })
                    
                    # Find SQLAlchemy models
                    models = re.findall(model_pattern, content)
                    for model in models:
                        self.results['database']['schema_tables'].append({
                            'name': model,
                            'file': file_info['path'],
                            'type': 'model'
                        })
            except Exception as e:
                print(f"  ⚠ Could not scan {file_info['path']}: {e}")
        
        # Find database references in code
        code_files = [f for f in self.results['files'] if f['type'] == 'code']
        query_patterns = [
            r'\.query\s*\(',
            r'SELECT.*FROM\s+(\w+)',
            r'INSERT INTO\s+(\w+)',
            r'UPDATE\s+(\w+)',
            r'DELETE FROM\s+(\w+)'
        ]
        
        for file_info in code_files:
            try:
                with open(file_info['full_path'], 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    for pattern in query_patterns:
                        if re.search(pattern, content, re.IGNORECASE):
                            self.results['database']['code_references'].append({
                                'file': file_info['path'],
                                'type': 'database_access'
                            })
                            break
            except Exception as e:
                pass
    
    def _scan_tests(self):
        """Scan and analyze test files"""
        test_files = [f for f in self.results['files'] 
                     if 'test' in f['path'].lower() and f['path'].endswith('.py')]
        
        for file_info in test_files:
            try:
                with open(file_info['full_path'], 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    # Count test functions
                    test_funcs = len(re.findall(r'def\s+test_\w+', content))
                    
                    # Check for async tests
                    async_tests = len(re.findall(r'async\s+def\s+test_\w+', content))
                    
                    self.results['tests'][file_info['path']] = {
                        'test_count': test_funcs,
                        'async_count': async_tests,
                        'size': file_info['size']
                    }
            except Exception as e:
                print(f"  ⚠ Could not scan {file_info['path']}: {e}")
    
    def _scan_dependencies(self):
        """Analyze dependencies from requirements.txt and package.json"""
        # Python dependencies
        req_files = [f for f in self.results['files'] 
                    if f['path'].endswith('requirements.txt') or f['path'].endswith('pyproject.toml')]
        
        for file_info in req_files:
            try:
                with open(file_info['full_path'], 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Simple parsing - extract package names
                    for line in content.split('\n'):
                        line = line.strip()
                        if line and not line.startswith('#'):
                            pkg = line.split('==')[0].split('>=')[0].split('<=')[0].strip()
                            if pkg:
                                self.results['dependencies']['documented'].append({
                                    'package': pkg,
                                    'type': 'python',
                                    'file': file_info['path']
                                })
            except Exception as e:
                print(f"  ⚠ Could not scan {file_info['path']}: {e}")
        
        # JavaScript dependencies
        pkg_files = [f for f in self.results['files'] if f['path'].endswith('package.json')]
        
        for file_info in pkg_files:
            try:
                with open(file_info['full_path'], 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
                    for pkg, version in deps.items():
                        self.results['dependencies']['documented'].append({
                            'package': pkg,
                            'version': version,
                            'type': 'javascript',
                            'file': file_info['path']
                        })
            except Exception as e:
                print(f"  ⚠ Could not scan {file_info['path']}: {e}")
    
    def _scan_config(self):
        """Scan configuration files"""
        config_files = [f for f in self.results['files'] if f['type'] == 'config']
        
        for file_info in config_files:
            try:
                with open(file_info['full_path'], 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    # Look for common config patterns
                    env_vars = re.findall(r'([A-Z_]+)\s*=', content)
                    
                    self.results['config'].append({
                        'path': file_info['path'],
                        'env_vars_count': len(env_vars),
                        'size': file_info['size']
                    })
            except Exception as e:
                print(f"  ⚠ Could not scan {file_info['path']}: {e}")
    
    def _detect_hallucinations(self):
        """Detect potential hallucinations - documented features not implemented"""
        # Compare documented API endpoints vs implemented
        doc_endpoints = {(e['method'], e['path']) for e in self.results['api_endpoints']['documented']}
        impl_endpoints = {(e['method'], e['path']) for e in self.results['api_endpoints']['implemented']}
        
        missing = doc_endpoints - impl_endpoints
        for method, path in missing:
            self.results['hallucinations'].append({
                'type': 'api_endpoint',
                'description': f'{method} {path} documented but not found in code',
                'severity': 'high'
            })
        
        # Check for documented database tables not in schema
        doc_files = [f for f in self.results['files'] if f['type'] == 'documentation']
        table_mentions = set()
        
        for file_info in doc_files:
            try:
                with open(file_info['full_path'], 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read().lower()
                    # Look for table name patterns
                    potential_tables = re.findall(r'\b(\w+)_table\b', content)
                    table_mentions.update(potential_tables)
            except:
                pass
        
        schema_tables = {t['name'].lower() for t in self.results['database']['schema_tables']}
        missing_tables = table_mentions - schema_tables
        
        for table in missing_tables:
            if len(table) > 3:  # Skip very short names
                self.results['hallucinations'].append({
                    'type': 'database_table',
                    'description': f'Table "{table}" mentioned in docs but not found in schema',
                    'severity': 'medium'
                })
    
    def _detect_drift(self):
        """Detect configuration drift"""
        # Compare .env.example vs actual .env patterns
        env_examples = [f for f in self.results['files'] if '.env.example' in f['path']]
        env_actuals = [f for f in self.results['files'] if f['path'].endswith('.env')]
        
        if env_examples and not env_actuals:
            self.results['drift'].append({
                'type': 'config',
                'description': 'Found .env.example but no actual .env file',
                'severity': 'high'
            })
        
        # Check for multiple versions of similar config files
        config_paths = [f['path'] for f in self.results['config']]
        config_names = defaultdict(list)
        
        for path in config_paths:
            name = Path(path).name
            config_names[name].append(path)
        
        for name, paths in config_names.items():
            if len(paths) > 1:
                self.results['drift'].append({
                    'type': 'config_duplication',
                    'description': f'Multiple {name} files found: {", ".join(paths)}',
                    'severity': 'medium'
                })
    
    def _scan_integrations(self):
        """Scan for external service integrations"""
        integration_patterns = {
            'gmail': r'gmail|google.*mail',
            'calendar': r'calendar',
            'stripe': r'stripe',
            'supabase': r'supabase',
            'openai': r'openai|gpt',
            'twilio': r'twilio',
            'firebase': r'firebase|firestore'
        }
        
        code_files = [f for f in self.results['files'] if f['type'] == 'code']
        
        for service, pattern in integration_patterns.items():
            files_with_integration = []
            for file_info in code_files:
                try:
                    with open(file_info['full_path'], 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read().lower()
                        if re.search(pattern, content):
                            files_with_integration.append(file_info['path'])
                except:
                    pass
            
            if files_with_integration:
                self.results['integration_points'].append({
                    'service': service,
                    'file_count': len(files_with_integration),
                    'files': files_with_integration[:5]  # First 5 only
                })
    
    def _generate_handoff(self):
        """Generate comprehensive handoff document"""
        report = []
        report.append("# MAYA PROJECT DEEP SCAN HANDOFF")
        report.append(f"**Generated:** {self.results['scan_time']}")
        report.append(f"**Scanner:** Claude Code")
        report.append(f"**For Analysis By:** Claude Desktop (Sonnet 4.5)")
        report.append("")
        report.append("=" * 80)
        report.append("")
        
        # Executive Summary
        report.append("## 📊 EXECUTIVE SUMMARY")
        report.append("")
        total_files = len(self.results['files'])
        code_files = len([f for f in self.results['files'] if f['type'] == 'code'])
        doc_files = len([f for f in self.results['files'] if f['type'] == 'documentation'])
        config_files = len([f for f in self.results['files'] if f['type'] == 'config'])
        
        report.append(f"- **Total Files Scanned:** {total_files}")
        report.append(f"- **Code Files:** {code_files}")
        report.append(f"- **Documentation Files:** {doc_files}")
        report.append(f"- **Configuration Files:** {config_files}")
        report.append(f"- **TODOs Found:** {len(self.results['todos'])}")
        report.append(f"- **FIXMEs/Bugs Found:** {len(self.results['fixmes'])}")
        report.append(f"- **Potential Hallucinations:** {len(self.results['hallucinations'])}")
        report.append(f"- **Drift Issues:** {len(self.results['drift'])}")
        report.append(f"- **Test Files:** {len(self.results['tests'])}")
        report.append("")
        
        # Hallucinations
        if self.results['hallucinations']:
            report.append("## 🚨 POTENTIAL HALLUCINATIONS")
            report.append("")
            report.append("Features documented but not found in implementation:")
            report.append("")
            for h in self.results['hallucinations']:
                severity_emoji = "🔴" if h['severity'] == 'high' else "🟡"
                report.append(f"{severity_emoji} **{h['type'].upper()}**: {h['description']}")
            report.append("")
        
        # Drift Issues
        if self.results['drift']:
            report.append("## 🔄 CONFIGURATION DRIFT")
            report.append("")
            for d in self.results['drift']:
                severity_emoji = "🔴" if d['severity'] == 'high' else "🟡"
                report.append(f"{severity_emoji} **{d['type'].upper()}**: {d['description']}")
            report.append("")
        
        # API Endpoints
        report.append("## 🔌 API ENDPOINTS")
        report.append("")
        report.append(f"**Documented:** {len(self.results['api_endpoints']['documented'])} endpoints")
        report.append(f"**Implemented:** {len(self.results['api_endpoints']['implemented'])} endpoints")
        report.append("")
        
        if self.results['api_endpoints']['implemented']:
            report.append("### Implemented Endpoints:")
            for ep in sorted(self.results['api_endpoints']['implemented'], key=lambda x: x['path'])[:20]:
                report.append(f"- `{ep['method']} {ep['path']}` ({ep['file']})")
            if len(self.results['api_endpoints']['implemented']) > 20:
                report.append(f"- ... and {len(self.results['api_endpoints']['implemented']) - 20} more")
            report.append("")
        
        # Database
        report.append("## 💾 DATABASE")
        report.append("")
        report.append(f"**Schema Tables/Models:** {len(self.results['database']['schema_tables'])}")
        report.append(f"**Code Files with DB Access:** {len(self.results['database']['code_references'])}")
        report.append("")
        
        if self.results['database']['schema_tables']:
            report.append("### Tables/Models:")
            for table in self.results['database']['schema_tables'][:15]:
                type_str = f" ({table.get('type', 'table')})" if 'type' in table else ""
                report.append(f"- `{table['name']}`{type_str} - {table['file']}")
            if len(self.results['database']['schema_tables']) > 15:
                report.append(f"- ... and {len(self.results['database']['schema_tables']) - 15} more")
            report.append("")
        
        # Tests
        report.append("## 🧪 TESTS")
        report.append("")
        total_tests = sum(t['test_count'] for t in self.results['tests'].values())
        report.append(f"**Total Test Functions:** {total_tests}")
        report.append(f"**Test Files:** {len(self.results['tests'])}")
        report.append("")
        
        for test_file, info in list(self.results['tests'].items())[:10]:
            report.append(f"- `{test_file}`: {info['test_count']} tests")
        if len(self.results['tests']) > 10:
            report.append(f"- ... and {len(self.results['tests']) - 10} more test files")
        report.append("")
        
        # Integrations
        if self.results['integration_points']:
            report.append("## 🔗 EXTERNAL INTEGRATIONS")
            report.append("")
            for integration in self.results['integration_points']:
                report.append(f"### {integration['service'].upper()}")
                report.append(f"Found in {integration['file_count']} files:")
                for f in integration['files']:
                    report.append(f"- `{f}`")
                report.append("")
        
        # TODOs
        if self.results['todos']:
            report.append("## 📝 TODOs")
            report.append("")
            report.append(f"Total: {len(self.results['todos'])}")
            report.append("")
            
            # Group by file
            todos_by_file = defaultdict(list)
            for todo in self.results['todos']:
                todos_by_file[todo['file']].append(todo)
            
            for file, todos in list(todos_by_file.items())[:15]:
                report.append(f"**{file}** ({len(todos)} TODOs):")
                for todo in todos[:3]:
                    report.append(f"  - Line {todo['line']}: `{todo['content'][:80]}`")
                if len(todos) > 3:
                    report.append(f"  - ... and {len(todos) - 3} more")
                report.append("")
            if len(todos_by_file) > 15:
                report.append(f"... and {len(todos_by_file) - 15} more files with TODOs")
            report.append("")
        
        # FIXMEs
        if self.results['fixmes']:
            report.append("## 🐛 FIXMEs & BUGS")
            report.append("")
            report.append(f"Total: {len(self.results['fixmes'])}")
            report.append("")
            
            for fixme in self.results['fixmes'][:20]:
                report.append(f"- **{fixme['file']}:{fixme['line']}**")
                report.append(f"  `{fixme['content'][:100]}`")
                report.append("")
            if len(self.results['fixmes']) > 20:
                report.append(f"... and {len(self.results['fixmes']) - 20} more")
            report.append("")
        
        # Dependencies
        report.append("## 📦 DEPENDENCIES")
        report.append("")
        python_deps = [d for d in self.results['dependencies']['documented'] if d['type'] == 'python']
        js_deps = [d for d in self.results['dependencies']['documented'] if d['type'] == 'javascript']
        
        report.append(f"**Python Packages:** {len(python_deps)}")
        report.append(f"**JavaScript Packages:** {len(js_deps)}")
        report.append("")
        
        # Configuration
        report.append("## ⚙️ CONFIGURATION")
        report.append("")
        report.append(f"**Config Files:** {len(self.results['config'])}")
        report.append("")
        for cfg in self.results['config'][:10]:
            report.append(f"- `{cfg['path']}` ({cfg['env_vars_count']} variables)")
        if len(self.results['config']) > 10:
            report.append(f"- ... and {len(self.results['config']) - 10} more")
        report.append("")
        
        # File Structure
        report.append("## 📁 PROJECT STRUCTURE")
        report.append("")
        report.append("### Key Directories:")
        
        # Group files by directory
        dirs = defaultdict(int)
        for file_info in self.results['files']:
            dir_path = str(Path(file_info['path']).parent)
            dirs[dir_path] += 1
        
        for dir_path, count in sorted(dirs.items(), key=lambda x: x[1], reverse=True)[:20]:
            report.append(f"- `{dir_path}/` ({count} files)")
        report.append("")
        
        # Critical Files
        report.append("## ⭐ CRITICAL FILES")
        report.append("")
        critical_patterns = ['main.py', 'app.py', 'index', 'config', 'settings', 'README']
        critical_files = []
        
        for pattern in critical_patterns:
            matching = [f for f in self.results['files'] if pattern in f['path'].lower()]
            critical_files.extend(matching[:3])
        
        for file_info in critical_files[:15]:
            report.append(f"- `{file_info['path']}` ({file_info['size']} bytes)")
        report.append("")
        
        # Summary Stats
        report.append("## 📈 STATISTICS")
        report.append("")
        total_size = sum(f['size'] for f in self.results['files'])
        avg_size = total_size / len(self.results['files']) if self.results['files'] else 0
        
        report.append(f"- **Total Project Size:** {total_size:,} bytes ({total_size / 1024 / 1024:.2f} MB)")
        report.append(f"- **Average File Size:** {avg_size:,.0f} bytes")
        report.append(f"- **Largest Files:**")
        
        largest = sorted(self.results['files'], key=lambda x: x['size'], reverse=True)[:5]
        for f in largest:
            report.append(f"  - `{f['path']}`: {f['size']:,} bytes")
        report.append("")
        
        # Recent Activity
        report.append("## 🕐 RECENT ACTIVITY")
        report.append("")
        recent = sorted(self.results['files'], key=lambda x: x['modified'] or '', reverse=True)[:10]
        report.append("Most recently modified files:")
        for f in recent:
            if f['modified']:
                report.append(f"- `{f['path']}` - {f['modified']}")
        report.append("")
        
        # Recommendations
        report.append("## 💡 RECOMMENDATIONS FOR CLAUDE DESKTOP")
        report.append("")
        report.append("Based on this scan, please analyze:")
        report.append("")
        report.append("1. **Hallucination Review**: Are the documented features actually implemented?")
        report.append("2. **Drift Analysis**: Do configurations match across environments?")
        report.append("3. **Progress Assessment**: What percentage of planned features are complete?")
        report.append("4. **Bug Priority**: Which FIXMEs should be addressed first?")
        report.append("5. **Technical Debt**: Are there patterns of incomplete implementations?")
        report.append("6. **Integration Health**: Are all external services properly integrated?")
        report.append("7. **Test Coverage**: Is testing adequate for the complexity level?")
        report.append("8. **Documentation Gap**: What's documented vs. what exists in code?")
        report.append("")
        
        # Save handoff
        handoff_path = self.root / "MAYA_DEEP_SCAN_HANDOFF.md"
        with open(handoff_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        
        # Save raw JSON for detailed analysis
        json_path = self.root / "MAYA_DEEP_SCAN_DATA.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n✅ Handoff document saved to: {handoff_path}")
        print(f"✅ Raw data saved to: {json_path}")
        print("\nReady for Claude Desktop analysis!")

if __name__ == "__main__":
    import sys
    
    # Get root directory from command line or use current directory
    root_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    
    print("\n" + "=" * 80)
    print("MAYA PROJECT DEEP SCANNER")
    print("Claude Code → Claude Desktop Handoff Tool")
    print("=" * 80)
    print(f"\nScanning: {os.path.abspath(root_dir)}")
    print("")
    
    scanner = MayaDeepScanner(root_dir)
    scanner.scan_all()
    
    print("\n" + "=" * 80)
    print("✅ SCAN COMPLETE!")
    print("=" * 80)
    print("\nNext Steps:")
    print("1. Review MAYA_DEEP_SCAN_HANDOFF.md")
    print("2. Send to Claude Desktop for analysis")
    print("3. Address identified issues based on priority")
    print("")
