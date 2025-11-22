"""
Reference Scanner - Finds all imports and path references
Part of MayAssistant Repository Restructure Safety System
"""

import os
import re
from pathlib import Path
import json


class ReferenceScanner:
    """Scans repository for all imports, paths, and references"""
    
    def __init__(self, repo_root):
        self.repo_root = Path(repo_root)
        self.references = {
            "python_imports": [],
            "config_paths": [],
            "documentation_links": [],
            "script_references": []
        }
    
    def scan_all(self):
        """Scan entire repository for references"""
        print("🔍 Scanning repository for all references...")
        
        self.scan_python_imports()
        self.scan_config_files()
        self.scan_documentation()
        self.scan_scripts()
        
        return self.references
    
    def scan_python_imports(self):
        """Scan Python files for imports"""
        print("   🐍 Scanning Python imports...")
        
        python_files = list(self.repo_root.rglob("*.py"))
        
        # Import patterns to match
        patterns = [
            r'^from\s+([\w\.]+)\s+import',  # from x import y
            r'^import\s+([\w\.]+)',          # import x
        ]
        
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    for line_num, line in enumerate(content.split('\n'), 1):
                        for pattern in patterns:
                            match = re.match(pattern, line.strip())
                            if match:
                                module = match.group(1)
                                # Check if it's a local import
                                if any(module.startswith(pkg) for pkg in ['backend', 'services', 'app']):
                                    self.references["python_imports"].append({
                                        "file": str(py_file.relative_to(self.repo_root)),
                                        "line": line_num,
                                        "import": module,
                                        "full_line": line.strip()
                                    })
            except Exception as e:
                print(f"      ⚠️  Could not scan {py_file}: {e}")
        
        print(f"      Found {len(self.references['python_imports'])} Python imports")
    
    def scan_config_files(self):
        """Scan configuration files for path references"""
        print("   ⚙️  Scanning configuration files...")
        
        config_patterns = [
            "**/*.json",
            "**/*.yaml",
            "**/*.yml",
            "**/*.toml",
            "**/Procfile",
            "**/.env*"
        ]
        
        for pattern in config_patterns:
            for config_file in self.repo_root.glob(pattern):
                if '.git' in str(config_file) or 'node_modules' in str(config_file):
                    continue
                
                try:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Look for path-like references
                    path_patterns = [
                        r'["\']([./][\w/.-]+)["\']',  # "./path" or "/path"
                        r'backend/[\w/.-]+',           # backend/something
                        r'services/[\w/.-]+',          # services/something
                    ]
                    
                    for line_num, line in enumerate(content.split('\n'), 1):
                        for pattern in path_patterns:
                            matches = re.findall(pattern, line)
                            for match in matches:
                                if 'backend' in match or 'services' in match:
                                    self.references["config_paths"].append({
                                        "file": str(config_file.relative_to(self.repo_root)),
                                        "line": line_num,
                                        "path": match,
                                        "full_line": line.strip()
                                    })
                except Exception as e:
                    print(f"      ⚠️  Could not scan {config_file}: {e}")
        
        print(f"      Found {len(self.references['config_paths'])} config path references")
    
    def scan_documentation(self):
        """Scan documentation for references"""
        print("   📚 Scanning documentation...")
        
        doc_files = list(self.repo_root.rglob("*.md"))
        
        for doc_file in doc_files:
            if '.git' in str(doc_file) or 'node_modules' in str(doc_file):
                continue
            
            try:
                with open(doc_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Look for file/directory references
                patterns = [
                    r'`([^`]+)`',                    # `code blocks`
                    r'\[([^\]]+)\]\(([^)]+)\)',      # [text](link)
                    r'backend/[\w/.-]+',
                    r'services/[\w/.-]+',
                ]
                
                for line_num, line in enumerate(content.split('\n'), 1):
                    for pattern in patterns:
                        matches = re.findall(pattern, line)
                        for match in matches:
                            ref = match if isinstance(match, str) else match[0]
                            if any(keyword in ref for keyword in ['backend', 'services', 'api', 'docs']):
                                self.references["documentation_links"].append({
                                    "file": str(doc_file.relative_to(self.repo_root)),
                                    "line": line_num,
                                    "reference": ref,
                                    "full_line": line.strip()[:100]  # Truncate long lines
                                })
            except Exception as e:
                print(f"      ⚠️  Could not scan {doc_file}: {e}")
        
        print(f"      Found {len(self.references['documentation_links'])} documentation references")
    
    def scan_scripts(self):
        """Scan shell scripts and batch files"""
        print("   📜 Scanning scripts...")
        
        script_patterns = ["**/*.sh", "**/*.ps1", "**/*.bat", "**/*.cmd"]
        
        for pattern in script_patterns:
            for script_file in self.repo_root.glob(pattern):
                if '.git' in str(script_file) or 'node_modules' in str(script_file):
                    continue
                
                try:
                    with open(script_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Look for path references
                    for line_num, line in enumerate(content.split('\n'), 1):
                        if any(keyword in line for keyword in ['backend', 'services', 'cd ', 'pushd']):
                            self.references["script_references"].append({
                                "file": str(script_file.relative_to(self.repo_root)),
                                "line": line_num,
                                "full_line": line.strip()
                            })
                except Exception as e:
                    print(f"      ⚠️  Could not scan {script_file}: {e}")
        
        print(f"      Found {len(self.references['script_references'])} script references")
    
    def save_report(self, output_file):
        """Save scan results to JSON file"""
        with open(output_file, 'w') as f:
            json.dump(self.references, f, indent=2)
        print(f"📄 Reference scan saved to: {output_file}")
    
    def get_summary(self):
        """Get summary of scan results"""
        total = sum(len(refs) for refs in self.references.values())
        return {
            "total_references": total,
            "python_imports": len(self.references["python_imports"]),
            "config_paths": len(self.references["config_paths"]),
            "documentation_links": len(self.references["documentation_links"]),
            "script_references": len(self.references["script_references"])
        }


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python reference_scanner.py <repo_root>")
        sys.exit(1)
    
    repo_root = sys.argv[1]
    scanner = ReferenceScanner(repo_root)
    
    references = scanner.scan_all()
    
    print("\n" + "="*70)
    print("📊 SCAN SUMMARY:")
    summary = scanner.get_summary()
    for key, value in summary.items():
        print(f"   {key}: {value}")
    
    output_file = Path(repo_root) / ".restructure_backups" / "reference_scan.json"
    output_file.parent.mkdir(exist_ok=True)
    scanner.save_report(output_file)
