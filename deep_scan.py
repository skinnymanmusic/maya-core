#!/usr/bin/env python3
"""
MAYA PROJECT DEEP SCAN
Comprehensive analysis of the entire maya-ai project
Produces a detailed handoff report for Claude Desktop to analyze
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

class MayaProjectScanner:
    def __init__(self, root_path):
        self.root = Path(root_path)
        self.results = {
            "scan_time": datetime.now().isoformat(),
            "project_root": str(root_path),
            "backend": {},
            "frontend": {},
            "documentation": {},
            "tests": {},
            "config": {},
            "issues": [],
            "hallucinations": [],
            "todos": [],
            "stats": defaultdict(int)
        }
        
    def scan_all(self):
        """Run all scans"""
        print("🔍 Starting comprehensive Maya project scan...")
        print()
        
        self.scan_backend()
        self.scan_frontend()
        self.scan_documentation()
        self.scan_tests()
        self.scan_config_files()
        self.detect_hallucinations()
        self.detect_drift()
        self.find_todos_fixmes()
        self.analyze_imports()
        self.check_integration()
        self.generate_report()
        
    def scan_backend(self):
        """Scan backend Python files"""
        print("📦 Scanning backend...")
        backend_path = self.root / "backend"
        
        if not backend_path.exists():
            self.results["backend"]["status"] = "NOT_FOUND"
            return
            
        backend_files = {
            "routers": [],
            "services": [],
            "models": [],
            "workers": [],
            "guardians": [],
            "migrations": [],
            "tests": [],
            "other": []
        }
        
        # Scan all Python files
        for py_file in backend_path.rglob("*.py"):
            if "node_modules" in str(py_file) or ".venv" in str(py_file):
                continue
                
            rel_path = py_file.relative_to(backend_path)
            file_info = self.analyze_python_file(py_file)
            
            # Categorize
            if "routers" in str(rel_path):
                backend_files["routers"].append(file_info)
            elif "services" in str(rel_path):
                backend_files["services"].append(file_info)
            elif "models" in str(rel_path):
                backend_files["models"].append(file_info)
            elif "workers" in str(rel_path):
                backend_files["workers"].append(file_info)
            elif "guardians" in str(rel_path):
                backend_files["guardians"].append(file_info)
            elif "tests" in str(rel_path):
                backend_files["tests"].append(file_info)
            else:
                backend_files["other"].append(file_info)
        
        # Scan migrations
        migrations_path = backend_path / "migrations"
        if migrations_path.exists():
            for sql_file in migrations_path.glob("*.sql"):
                backend_files["migrations"].append({
                    "path": str(sql_file.relative_to(backend_path)),
                    "name": sql_file.name,
                    "size": sql_file.stat().st_size
                })
        
        self.results["backend"] = backend_files
        self.results["stats"]["backend_files"] = sum(len(v) for v in backend_files.values())
        
    def analyze_python_file(self, path):
        """Analyze a Python file"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            return {"path": str(path), "error": "Could not read file"}
            
        lines = content.split('\n')
        
        # Detect patterns
        has_class = bool(re.search(r'^class\s+\w+', content, re.MULTILINE))
        has_async = 'async def' in content
        has_router = '@router.' in content
        has_tests = 'def test_' in content or 'async def test_' in content
        
        # Count imports
        imports = len([l for l in lines if l.strip().startswith('import ') or l.strip().startswith('from ')])
        
        # Find TODOs/FIXMEs
        todos = [line.strip() for line in lines if 'TODO' in line.upper() or 'FIXME' in line.upper()]
        
        # Check if stub (very short with mostly imports/types)
        is_stub = len(lines) < 50 and imports > len([l for l in lines if l.strip() and not l.strip().startswith('#')])
        
        return {
            "path": str(path.relative_to(self.root)),
            "lines": len(lines),
            "size": path.stat().st_size,
            "has_class": has_class,
            "has_async": has_async,
            "has_router": has_router,
            "has_tests": has_tests,
            "imports": imports,
            "todos": todos,
            "is_stub": is_stub,
            "empty": len(content.strip()) == 0
        }
    
    def scan_frontend(self):
        """Scan frontend TypeScript/React files"""
        print("🎨 Scanning frontend...")
        frontend_path = self.root / "omega-frontend"
        
        if not frontend_path.exists():
            self.results["frontend"]["status"] = "NOT_FOUND"
            return
            
        frontend_files = {
            "pages": [],
            "components": [],
            "lib": [],
            "types": [],
            "other": []
        }
        
        # Scan TypeScript/TSX files
        for ts_file in frontend_path.rglob("*.ts*"):
            if "node_modules" in str(ts_file) or ".next" in str(ts_file):
                continue
                
            rel_path = ts_file.relative_to(frontend_path)
            file_info = self.analyze_typescript_file(ts_file)
            
            # Categorize
            if "page.tsx" in ts_file.name:
                frontend_files["pages"].append(file_info)
            elif "components" in str(rel_path):
                frontend_files["components"].append(file_info)
            elif "lib" in str(rel_path):
                frontend_files["lib"].append(file_info)
            elif "types" in str(rel_path) or ts_file.suffix == ".d.ts":
                frontend_files["types"].append(file_info)
            else:
                frontend_files["other"].append(file_info)
        
        self.results["frontend"] = frontend_files
        self.results["stats"]["frontend_files"] = sum(len(v) for v in frontend_files.values())
        
    def analyze_typescript_file(self, path):
        """Analyze a TypeScript file"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            return {"path": str(path), "error": "Could not read file"}
            
        lines = content.split('\n')
        
        # Detect patterns
        has_export = 'export' in content
        has_component = 'export default' in content or 'export const' in content
        has_hooks = 'useState' in content or 'useEffect' in content
        has_api_call = 'fetch(' in content or 'axios' in content
        
        # Count imports
        imports = len([l for l in lines if l.strip().startswith('import ')])
        
        # Find TODOs
        todos = [line.strip() for line in lines if 'TODO' in line.upper()]
        
        # Check if stub
        is_stub = len(lines) < 30 and todos and not has_component
        
        return {
            "path": str(path.relative_to(self.root)),
            "lines": len(lines),
            "size": path.stat().st_size,
            "has_export": has_export,
            "has_component": has_component,
            "has_hooks": has_hooks,
            "has_api_call": has_api_call,
            "imports": imports,
            "todos": todos,
            "is_stub": is_stub,
            "empty": len(content.strip()) == 0
        }
    
    def scan_documentation(self):
        """Scan all markdown documentation"""
        print("📚 Scanning documentation...")
        
        docs = {
            "core_docs": [],
            "reports": [],
            "notes": [],
            "other": []
        }
        
        for md_file in self.root.rglob("*.md"):
            if "node_modules" in str(md_file) or ".next" in str(md_file):
                continue
                
            rel_path = md_file.relative_to(self.root)
            
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
            except:
                continue
                
            info = {
                "path": str(rel_path),
                "name": md_file.name,
                "size": md_file.stat().st_size,
                "lines": len(content.split('\n')),
                "word_count": len(content.split())
            }
            
            # Categorize
            if "docs/" in str(rel_path) and "reports" not in str(rel_path):
                docs["core_docs"].append(info)
            elif "reports" in str(rel_path):
                docs["reports"].append(info)
            elif "notes" in str(rel_path):
                docs["notes"].append(info)
            else:
                docs["other"].append(info)
        
        self.results["documentation"] = docs
        self.results["stats"]["documentation_files"] = sum(len(v) for v in docs.values())
        
    def scan_tests(self):
        """Scan all test files"""
        print("🧪 Scanning tests...")
        
        tests = {
            "backend_tests": [],
            "frontend_tests": [],
            "integration_tests": []
        }
        
        # Backend tests
        backend_tests = self.root / "backend" / "tests"
        if backend_tests.exists():
            for test_file in backend_tests.rglob("test_*.py"):
                try:
                    with open(test_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    test_count = len(re.findall(r'def test_\w+|async def test_\w+', content))
                    
                    tests["backend_tests"].append({
                        "path": str(test_file.relative_to(self.root)),
                        "test_count": test_count,
                        "lines": len(content.split('\n'))
                    })
                except:
                    pass
        
        # Frontend tests
        frontend = self.root / "omega-frontend"
        if frontend.exists():
            for test_file in frontend.rglob("*.test.ts*"):
                try:
                    with open(test_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    test_count = len(re.findall(r"it\(|test\(|describe\(", content))
                    
                    tests["frontend_tests"].append({
                        "path": str(test_file.relative_to(self.root)),
                        "test_count": test_count,
                        "lines": len(content.split('\n'))
                    })
                except:
                    pass
        
        self.results["tests"] = tests
        
    def scan_config_files(self):
        """Scan configuration files"""
        print("⚙️  Scanning configuration files...")
        
        config_files = []
        
        config_patterns = [
            "*.json",
            "*.yaml", 
            "*.yml",
            "*.toml",
            ".env*",
            "Procfile",
            "railway.toml",
            "vercel.json",
            "package.json",
            "tsconfig.json",
            "pytest.ini",
            "pyproject.toml"
        ]
        
        for pattern in config_patterns:
            for config_file in self.root.rglob(pattern):
                if "node_modules" in str(config_file) or ".next" in str(config_file):
                    continue
                    
                config_files.append({
                    "path": str(config_file.relative_to(self.root)),
                    "name": config_file.name,
                    "size": config_file.stat().st_size
                })
        
        self.results["config"] = config_files
        
    def detect_hallucinations(self):
        """Detect references to files/modules that don't exist"""
        print("🔎 Detecting hallucinations...")
        
        hallucinations = []
        
        # Check documentation for references to missing files
        for md_file in self.root.rglob("*.md"):
            if "node_modules" in str(md_file):
                continue
                
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find code references
                file_refs = re.findall(r'`([^`]+\.(py|tsx?|json|sql))`', content)
                
                for ref, _ in file_refs:
                    # Check if file exists
                    potential_paths = [
                        self.root / ref,
                        self.root / "backend" / ref,
                        self.root / "omega-frontend" / ref
                    ]
                    
                    if not any(p.exists() for p in potential_paths):
                        hallucinations.append({
                            "type": "missing_file",
                            "doc": str(md_file.relative_to(self.root)),
                            "reference": ref,
                            "context": "Documentation references non-existent file"
                        })
            except:
                pass
        
        self.results["hallucinations"] = hallucinations[:50]  # Limit to first 50
        
    def detect_drift(self):
        """Detect inconsistencies between docs and code"""
        print("📊 Detecting drift...")
        
        drift_issues = []
        
        # Check if documented features are actually implemented
        features_claimed = set()
        features_found = set()
        
        # Scan docs for claimed features
        for md_file in (self.root / "docs").rglob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find "implemented" or "complete" claims
                if "✅" in content or "COMPLETE" in content:
                    # Extract feature names (simplified)
                    claimed = re.findall(r'✅\s+([^\n]+)', content)
                    features_claimed.update(claimed)
            except:
                pass
        
        # Compare with actual code
        # This is simplified - just checking if routers exist for claimed features
        
        self.results["drift"] = {
            "claimed_features": len(features_claimed),
            "issues": drift_issues[:20]  # Limit
        }
        
    def find_todos_fixmes(self):
        """Find all TODOs and FIXMEs across project"""
        print("📝 Finding TODOs and FIXMEs...")
        
        todos = []
        
        for file_path in self.root.rglob("*"):
            if file_path.is_file() and file_path.suffix in ['.py', '.ts', '.tsx', '.js', '.jsx', '.md']:
                if "node_modules" in str(file_path) or ".next" in str(file_path):
                    continue
                    
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    
                    for i, line in enumerate(lines, 1):
                        if 'TODO' in line.upper() or 'FIXME' in line.upper():
                            todos.append({
                                "file": str(file_path.relative_to(self.root)),
                                "line": i,
                                "content": line.strip()
                            })
                except:
                    pass
        
        self.results["todos"] = todos[:100]  # Limit to first 100
        
    def analyze_imports(self):
        """Analyze import dependencies"""
        print("🔗 Analyzing imports and dependencies...")
        
        # Check for circular imports (simplified)
        backend_imports = defaultdict(list)
        
        for py_file in (self.root / "backend").rglob("*.py"):
            if "tests" in str(py_file):
                continue
                
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                imports = re.findall(r'from app\.(\w+)', content)
                backend_imports[py_file.name].extend(imports)
            except:
                pass
        
        self.results["stats"]["backend_import_graph"] = len(backend_imports)
        
    def check_integration(self):
        """Check frontend-backend integration"""
        print("🔌 Checking integration points...")
        
        # Find API calls in frontend
        api_calls = set()
        
        frontend = self.root / "omega-frontend"
        if frontend.exists():
            for ts_file in frontend.rglob("*.ts*"):
                if "node_modules" in str(ts_file):
                    continue
                    
                try:
                    with open(ts_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Find API endpoint calls
                    endpoints = re.findall(r"['\"]/(api/[^'\"]+)['\"]", content)
                    api_calls.update(endpoints)
                except:
                    pass
        
        # Find backend routes
        backend_routes = set()
        backend = self.root / "backend"
        if backend.exists():
            for py_file in (backend / "app" / "routers").rglob("*.py"):
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    routes = re.findall(r'@router\.(get|post|put|delete)\(["\']([^"\']+)', content)
                    backend_routes.update(route for _, route in routes)
                except:
                    pass
        
        self.results["integration"] = {
            "frontend_api_calls": len(api_calls),
            "backend_routes": len(backend_routes),
            "api_calls_sample": list(api_calls)[:10],
            "backend_routes_sample": list(backend_routes)[:10]
        }
        
    def generate_report(self):
        """Generate comprehensive markdown report"""
        print("📄 Generating report...")
        
        report = []
        report.append("# MAYA PROJECT DEEP SCAN REPORT")
        report.append(f"**Scan Date:** {self.results['scan_time']}")
        report.append(f"**Project Root:** {self.results['project_root']}")
        report.append("")
        report.append("---")
        report.append("")
        
        # Executive Summary
        report.append("## 📊 EXECUTIVE SUMMARY")
        report.append("")
        report.append(f"- **Backend Files:** {self.results['stats'].get('backend_files', 0)}")
        report.append(f"- **Frontend Files:** {self.results['stats'].get('frontend_files', 0)}")
        report.append(f"- **Documentation Files:** {self.results['stats'].get('documentation_files', 0)}")
        report.append(f"- **TODOs Found:** {len(self.results['todos'])}")
        report.append(f"- **Hallucinations Detected:** {len(self.results['hallucinations'])}")
        report.append("")
        
        # Backend Analysis
        report.append("## 🔧 BACKEND ANALYSIS")
        report.append("")
        backend = self.results["backend"]
        
        report.append(f"### Routers ({len(backend.get('routers', []))})")
        for router in backend.get('routers', []):
            status = "✅" if not router.get('is_stub') and not router.get('empty') else "⚠️"
            report.append(f"- {status} `{router['path']}` ({router['lines']} lines)")
        report.append("")
        
        report.append(f"### Services ({len(backend.get('services', []))})")
        for service in backend.get('services', [])[:15]:  # Limit to 15
            status = "✅" if not service.get('is_stub') and not service.get('empty') else "⚠️"
            report.append(f"- {status} `{service['path']}` ({service['lines']} lines)")
        if len(backend.get('services', [])) > 15:
            report.append(f"- ... and {len(backend.get('services', [])) - 15} more")
        report.append("")
        
        report.append(f"### Guardians ({len(backend.get('guardians', []))})")
        for guardian in backend.get('guardians', []):
            status = "✅" if guardian.get('has_class') else "⚠️"
            report.append(f"- {status} `{guardian['path']}` ({guardian['lines']} lines)")
        report.append("")
        
        report.append(f"### Workers ({len(backend.get('workers', []))})")
        for worker in backend.get('workers', []):
            report.append(f"- ✅ `{worker['path']}` ({worker['lines']} lines)")
        report.append("")
        
        report.append(f"### Migrations ({len(backend.get('migrations', []))})")
        for migration in backend.get('migrations', []):
            report.append(f"- ✅ `{migration['path']}`")
        report.append("")
        
        # Frontend Analysis
        report.append("## 🎨 FRONTEND ANALYSIS")
        report.append("")
        frontend = self.results["frontend"]
        
        report.append(f"### Pages ({len(frontend.get('pages', []))})")
        if frontend.get('pages'):
            for page in frontend.get('pages', []):
                status = "✅" if not page.get('is_stub') and not page.get('empty') else "❌"
                report.append(f"- {status} `{page['path']}` ({page['lines']} lines)")
        else:
            report.append("- ⚠️ **NO PAGES FOUND** - Frontend appears empty")
        report.append("")
        
        report.append(f"### Components ({len(frontend.get('components', []))})")
        for comp in frontend.get('components', [])[:10]:
            status = "✅" if not comp.get('is_stub') and not comp.get('empty') else "⚠️"
            report.append(f"- {status} `{comp['path']}` ({comp['lines']} lines)")
        if len(frontend.get('components', [])) > 10:
            report.append(f"- ... and {len(frontend.get('components', [])) - 10} more")
        report.append("")
        
        # Documentation
        report.append("## 📚 DOCUMENTATION")
        report.append("")
        docs = self.results["documentation"]
        
        report.append(f"### Core Documentation ({len(docs.get('core_docs', []))})")
        for doc in docs.get('core_docs', []):
            report.append(f"- `{doc['path']}` ({doc['word_count']:,} words)")
        report.append("")
        
        report.append(f"### Reports ({len(docs.get('reports', []))})")
        for doc in docs.get('reports', [])[:10]:
            report.append(f"- `{doc['path']}` ({doc['word_count']:,} words)")
        if len(docs.get('reports', [])) > 10:
            report.append(f"- ... and {len(docs.get('reports', [])) - 10} more")
        report.append("")
        
        # Tests
        report.append("## 🧪 TESTS")
        report.append("")
        tests = self.results["tests"]
        
        total_backend_tests = sum(t['test_count'] for t in tests.get('backend_tests', []))
        report.append(f"### Backend Tests")
        report.append(f"- **Files:** {len(tests.get('backend_tests', []))}")
        report.append(f"- **Total Tests:** {total_backend_tests}")
        report.append("")
        
        total_frontend_tests = sum(t['test_count'] for t in tests.get('frontend_tests', []))
        report.append(f"### Frontend Tests")
        report.append(f"- **Files:** {len(tests.get('frontend_tests', []))}")
        report.append(f"- **Total Tests:** {total_frontend_tests}")
        report.append("")
        
        # Issues
        report.append("## ⚠️ ISSUES DETECTED")
        report.append("")
        
        report.append(f"### Hallucinations ({len(self.results['hallucinations'])})")
        for h in self.results['hallucinations'][:20]:
            report.append(f"- `{h['doc']}` references missing file: `{h['reference']}`")
        if len(self.results['hallucinations']) > 20:
            report.append(f"- ... and {len(self.results['hallucinations']) - 20} more")
        report.append("")
        
        report.append(f"### TODOs ({len(self.results['todos'])})")
        # Group by file
        todos_by_file = defaultdict(list)
        for todo in self.results['todos']:
            todos_by_file[todo['file']].append(todo)
        
        for file, todos in list(todos_by_file.items())[:15]:
            report.append(f"- `{file}` ({len(todos)} TODOs)")
            for todo in todos[:3]:
                report.append(f"  - Line {todo['line']}: {todo['content'][:80]}")
        if len(todos_by_file) > 15:
            report.append(f"- ... and {len(todos_by_file) - 15} more files with TODOs")
        report.append("")
        
        # Integration
        report.append("## 🔌 INTEGRATION STATUS")
        report.append("")
        integration = self.results["integration"]
        report.append(f"- **Frontend API Calls:** {integration['frontend_api_calls']}")
        report.append(f"- **Backend Routes:** {integration['backend_routes']}")
        report.append("")
        
        if integration.get('api_calls_sample'):
            report.append("**Frontend calls these endpoints:**")
            for call in integration['api_calls_sample']:
                report.append(f"- `{call}`")
            report.append("")
        
        if integration.get('backend_routes_sample'):
            report.append("**Backend provides these routes:**")
            for route in integration['backend_routes_sample']:
                report.append(f"- `{route}`")
            report.append("")
        
        # Configuration
        report.append("## ⚙️ CONFIGURATION FILES")
        report.append("")
        for config in self.results['config'][:20]:
            report.append(f"- `{config['path']}`")
        if len(self.results['config']) > 20:
            report.append(f"- ... and {len(self.results['config']) - 20} more")
        report.append("")
        
        # Write report
        report_path = self.root / "MAYA_DEEP_SCAN_REPORT.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        
        print("")
        print("=" * 80)
        print("✅ SCAN COMPLETE!")
        print("=" * 80)
        print(f"📄 Report saved to: {report_path}")
        print("")
        print("KEY FINDINGS:")
        print(f"  - Backend files: {self.results['stats'].get('backend_files', 0)}")
        print(f"  - Frontend files: {self.results['stats'].get('frontend_files', 0)}")
        print(f"  - TODOs: {len(self.results['todos'])}")
        print(f"  - Hallucinations: {len(self.results['hallucinations'])}")
        print("")

if __name__ == "__main__":
    scanner = MayaProjectScanner(".")
    scanner.scan_all()
