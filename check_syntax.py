#!/usr/bin/env python3
"""
Syntax checker for Python files in the project
"""

import ast
import sys
import os

def check_python_syntax(file_path):
    """Check if a Python file has valid syntax"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        
        # Parse the AST to check syntax
        ast.parse(source, filename=file_path)
        return True, None
    except SyntaxError as e:
        return False, f"Syntax error: {e}"
    except Exception as e:
        return False, f"Error reading file: {e}"

def main():
    """Check syntax of all Python files in the project"""
    python_files = [
        'app.py',
        'run.py',
        'test_installation.py',
        'check_syntax.py'
    ]
    
    print("🔍 Checking Python syntax...")
    print("=" * 40)
    
    all_valid = True
    
    for file_path in python_files:
        if os.path.exists(file_path):
            valid, error = check_python_syntax(file_path)
            if valid:
                print(f"✓ {file_path}: Valid syntax")
            else:
                print(f"✗ {file_path}: {error}")
                all_valid = False
        else:
            print(f"⚠ {file_path}: File not found")
    
    print("=" * 40)
    if all_valid:
        print("🎉 All Python files have valid syntax!")
        return 0
    else:
        print("❌ Some files have syntax errors!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
