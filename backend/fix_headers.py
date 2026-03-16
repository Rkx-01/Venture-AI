import os
import glob
import subprocess

def fix_file(path):
    with open(path, 'r') as f:
        lines = f.readlines()
        
    # We want to put `from __future__ import annotations` as line 1
    # and then the `"""docstring"""` if it exists.
    # OR we just use `ruff format` and `ruff check --fix`.
    # Let's see if we can just move `from __future__ import annotations` and the docstring 
    # to the top of the file before any other imports.
    
    # 1. extract docstring (if exists at top)
    # 2. extract `from __future__ import annotations`
    # 3. put future first, then docstrings, then everything else.
    
    future_import = "from __future__ import annotations\n"
    
    # extract docstring
    in_docstring = False
    docstring_lines = []
    other_lines = []
    
    has_future = False
    
    # find docstring at top
    idx = 0
    while idx < len(lines):
        line = lines[idx]
        if line.strip() == "from __future__ import annotations":
            has_future = True
            idx += 1
            continue
            
        if line.strip().startswith('"""') and not in_docstring:
            in_docstring = True
            docstring_lines.append(line)
            if line.strip() != '"""' and line.strip().endswith('"""') and len(line.strip()) > 3:
                in_docstring = False # single line docstring
            # Check if it's just `"""` or `""" ... """`
            elif line.strip() == '"""' and docstring_lines.count('"""') == 2:
                # Wait, count('"""') checking won't work perfectly on first line
                pass
            
            # Better docstring parsing
            pass
            
        # simpler approach: just read the whole file as a string
        idx += 1
        
def fix_entire_file(path):
    with open(path, 'r') as f:
        content = f.read()
        
    if '"""' not in content:
        return
        
    parts = content.split('"""')
    # if the file has a docstring near the top
    # The first part is usually empty or just `from __future__...`
    # Let's use ast to parse and rewrite!
    
import ast
def fix_with_ast(path):
    with open(path, 'r') as f:
        source = f.read()
    
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return # Skip files with syntax errors
        
    docstring = ast.get_docstring(tree)
    
    # Actually AST is destructive to comments. 
    # Hand-parsing is better.
    pass

def simple_fix(path):
    with open(path, 'r') as f:
        lines = f.readlines()
        
    # Remove all `from __future__ import annotations`
    filtered_lines = [l for l in lines if l.strip() != "from __future__ import annotations"]
    
    # Insert it at the very top
    filtered_lines.insert(0, "from __future__ import annotations\n")
    
    with open(path, 'w') as f:
        f.writelines(filtered_lines)

for root, _, files in os.walk('app'):
    for file in files:
        if file.endswith('.py'):
            simple_fix(os.path.join(root, file))

print("Fixed future imports. Running ruff fix...")
subprocess.run(["venv/bin/ruff", "check", "--fix", "app"])
