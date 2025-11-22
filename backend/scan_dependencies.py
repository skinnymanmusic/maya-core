"""
Comprehensive dependency scanner for Maya backend
Finds all imports and checks against requirements.txt
"""
import os
import re
from pathlib import Path
from collections import defaultdict

def extract_imports(file_path):
    """Extract all import statements from a Python file"""
    imports = set()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Find all import statements
        # Pattern 1: import module
        pattern1 = r'^import\s+([a-zA-Z0-9_]+)'
        # Pattern 2: from module import ...
        pattern2 = r'^from\s+([a-zA-Z0-9_]+)'
        
        for line in content.split('\n'):
            line = line.strip()
            
            # Skip comments
            if line.startswith('#'):
                continue
                
            # Match import patterns
            match1 = re.match(pattern1, line)
            match2 = re.match(pattern2, line)
            
            if match1:
                imports.add(match1.group(1))
            elif match2:
                imports.add(match2.group(1))
                
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        
    return imports

def scan_directory(directory):
    """Recursively scan directory for Python files"""
    all_imports = set()
    file_count = 0
    
    for root, dirs, files in os.walk(directory):
        # Skip certain directories
        skip_dirs = {'__pycache__', 'venv', '.venv', 'node_modules', '.pytest_cache', 'archive'}
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                imports = extract_imports(file_path)
                all_imports.update(imports)
                file_count += 1
                
    return all_imports, file_count

def parse_requirements(req_file):
    """Parse requirements.txt to get installed packages"""
    packages = set()
    try:
        with open(req_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if line and not line.startswith('#'):
                    # Extract package name (before ==, >=, etc.)
                    package = re.split(r'[=<>!]', line)[0].strip()
                    # Handle extras like uvicorn[standard]
                    package = package.split('[')[0]
                    packages.add(package.lower())
    except Exception as e:
        print(f"Error reading requirements.txt: {e}")
        
    return packages

# Standard library modules (don't need to be in requirements.txt)
STDLIB_MODULES = {
    'abc', 'aifc', 'argparse', 'array', 'ast', 'asyncio', 'atexit', 'audioop',
    'base64', 'bdb', 'binascii', 'binhex', 'bisect', 'builtins', 'bz2',
    'calendar', 'cgi', 'cgitb', 'chunk', 'cmath', 'cmd', 'code', 'codecs',
    'codeop', 'collections', 'colorsys', 'compileall', 'concurrent', 'configparser',
    'contextlib', 'contextvars', 'copy', 'copyreg', 'cProfile', 'csv', 'ctypes',
    'curses', 'dataclasses', 'datetime', 'dbm', 'decimal', 'difflib', 'dis',
    'distutils', 'doctest', 'email', 'encodings', 'enum', 'errno', 'faulthandler',
    'fcntl', 'filecmp', 'fileinput', 'fnmatch', 'formatter', 'fractions', 'ftplib',
    'functools', 'gc', 'getopt', 'getpass', 'gettext', 'glob', 'graphlib', 'grp',
    'gzip', 'hashlib', 'heapq', 'hmac', 'html', 'http', 'imaplib', 'imghdr',
    'imp', 'importlib', 'inspect', 'io', 'ipaddress', 'itertools', 'json',
    'keyword', 'lib2to3', 'linecache', 'locale', 'logging', 'lzma', 'mailbox',
    'mailcap', 'marshal', 'math', 'mimetypes', 'mmap', 'modulefinder', 'msilib',
    'msvcrt', 'multiprocessing', 'netrc', 'nis', 'nntplib', 'numbers', 'operator',
    'optparse', 'os', 'ossaudiodev', 'parser', 'pathlib', 'pdb', 'pickle',
    'pickletools', 'pipes', 'pkgutil', 'platform', 'plistlib', 'poplib', 'posix',
    'posixpath', 'pprint', 'profile', 'pstats', 'pty', 'pwd', 'py_compile',
    'pyclbr', 'pydoc', 'queue', 'quopri', 'random', 're', 'readline', 'reprlib',
    'resource', 'rlcompleter', 'runpy', 'sched', 'secrets', 'select', 'selectors',
    'shelve', 'shlex', 'shutil', 'signal', 'site', 'smtpd', 'smtplib', 'sndhdr',
    'socket', 'socketserver', 'spwd', 'sqlite3', 'ssl', 'stat', 'statistics',
    'string', 'stringprep', 'struct', 'subprocess', 'sunau', 'symbol', 'symtable',
    'sys', 'sysconfig', 'syslog', 'tabnanny', 'tarfile', 'telnetlib', 'tempfile',
    'termios', 'test', 'textwrap', 'threading', 'time', 'timeit', 'tkinter',
    'token', 'tokenize', 'trace', 'traceback', 'tracemalloc', 'tty', 'turtle',
    'turtledemo', 'types', 'typing', 'unicodedata', 'unittest', 'urllib', 'uu',
    'uuid', 'venv', 'warnings', 'wave', 'weakref', 'webbrowser', 'winreg',
    'winsound', 'wsgiref', 'xdrlib', 'xml', 'xmlrpc', 'zipapp', 'zipfile',
    'zipimport', 'zlib', 'zoneinfo'
}

# Common package name mappings (import name -> package name)
PACKAGE_MAPPINGS = {
    'PIL': 'pillow',
    'cv2': 'opencv-python',
    'yaml': 'pyyaml',
    'dotenv': 'python-dotenv',
    'jwt': 'pyjwt',
    'dateutil': 'python-dateutil',
    'google': 'google-auth',
    'googleapiclient': 'google-api-python-client',
    'slowapi': 'slowapi',
}

def main():
    backend_dir = r'C:\Users\delin\maya-ai\backend\app'
    req_file = r'C:\Users\delin\maya-ai\backend\requirements.txt'
    
    print("🔍 Scanning Maya backend for dependencies...\n")
    
    # Scan all Python files
    all_imports, file_count = scan_directory(backend_dir)
    print(f"✅ Scanned {file_count} Python files")
    print(f"📦 Found {len(all_imports)} unique imports\n")
    
    # Parse requirements.txt
    installed_packages = parse_requirements(req_file)
    print(f"📋 Found {len(installed_packages)} packages in requirements.txt\n")
    
    # Filter out local imports (app.*)
    external_imports = {imp for imp in all_imports if not imp.startswith('app')}
    
    # Filter out standard library
    third_party = external_imports - STDLIB_MODULES
    
    # Map import names to package names
    mapped_packages = set()
    for imp in third_party:
        package_name = PACKAGE_MAPPINGS.get(imp, imp.lower())
        mapped_packages.add(package_name)
    
    # Find missing packages
    missing = mapped_packages - installed_packages
    
    if missing:
        print("❌ MISSING DEPENDENCIES FOUND:\n")
        for pkg in sorted(missing):
            print(f"  • {pkg}")
        print(f"\n🔢 Total missing: {len(missing)} packages")
    else:
        print("✅ All dependencies are installed!")
        
    # Show some stats
    print(f"\n📊 Statistics:")
    print(f"  • Total imports: {len(all_imports)}")
    print(f"  • External imports: {len(external_imports)}")
    print(f"  • Third-party packages: {len(third_party)}")
    print(f"  • Already installed: {len(installed_packages)}")
    print(f"  • Missing: {len(missing)}")
    
    return missing

if __name__ == '__main__':
    missing = main()
