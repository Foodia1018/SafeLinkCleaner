import os
import re
import sys

def find_python_files(directory):
    """Find all Python files in the directory"""
    python_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files

def extract_imports(file_path):
    """Extract import statements from a Python file"""
    imports = []
    import_re = re.compile(r'^\s*(?:from\s+([\w\.]+)\s+import|import\s+([\w\.,\s]+))')
    
    with open(file_path, 'r') as f:
        try:
            for line in f:
                match = import_re.match(line)
                if match:
                    # Handle 'from X import Y' style
                    if match.group(1):
                        base_module = match.group(1).split('.')[0]
                        if base_module != '__future__':
                            imports.append(base_module)
                    # Handle 'import X, Y, Z' style
                    elif match.group(2):
                        modules = [m.strip().split('.')[0] for m in match.group(2).split(',')]
                        imports.extend([m for m in modules if m != '__future__'])
        except UnicodeDecodeError:
            print(f"Warning: Could not read {file_path} due to encoding issues")
    
    return imports

def is_standard_library(module):
    """Check if a module is part of the Python standard library"""
    standard_libs = {
        # This is not exhaustive but covers common standard library modules
        'abc', 'argparse', 'array', 'ast', 'asyncio', 'base64', 'bisect', 'calendar',
        'collections', 'concurrent', 'contextlib', 'copy', 'csv', 'datetime', 'decimal',
        'difflib', 'enum', 'fnmatch', 'functools', 'glob', 'gzip', 'hashlib', 'heapq',
        'hmac', 'html', 'http', 'importlib', 'inspect', 'io', 'itertools', 'json',
        'logging', 'math', 'multiprocessing', 'operator', 'os', 'pathlib', 'pickle',
        'platform', 'pprint', 'queue', 'random', 're', 'shutil', 'signal', 'socket',
        'sqlite3', 'statistics', 'string', 'struct', 'subprocess', 'sys', 'tempfile',
        'threading', 'time', 'types', 'typing', 'unittest', 'urllib', 'uuid', 'warnings',
        'weakref', 'xml', 'zipfile', 'zlib'
    }
    return module in standard_libs

def analyze_project_imports(directory='.'):
    """Analyze imports from all Python files in the project"""
    python_files = find_python_files(directory)
    all_imports = []
    
    for file in python_files:
        imports = extract_imports(file)
        all_imports.extend(imports)
    
    # Count occurrences of each import
    import_counts = {}
    for module in all_imports:
        import_counts[module] = import_counts.get(module, 0) + 1
    
    # Filter out standard library imports
    external_modules = {module: count for module, count in import_counts.items() 
                         if not is_standard_library(module)}
    
    # Sort by frequency
    sorted_modules = sorted(external_modules.items(), key=lambda x: (-x[1], x[0]))
    
    print("\nRequired Third-Party Modules:")
    for module, count in sorted_modules:
        print(f"- {module} (used {count} times)")

if __name__ == "__main__":
    analyze_project_imports()
