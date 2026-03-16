import os
import ast

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
        
    try:
        ast.parse(content)
        return # File is syntactically valid
    except SyntaxError:
        pass
        
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    # We messed up by removing `"""` and putting lines without them.
    # The fix_docstrings.py did:
    # new_content += "".join(docstring_lines)
    # new_content += '"""\n'
    # So the start of the docstring is missing its `"""`.
    
    if lines and lines[0].startswith('from __future__ import annotations'):
        lines.insert(1, '"""\n')
    else:
        lines.insert(0, '"""\n')
        
    # Test if this simple fix makes it valid
    test_content = "".join(lines)
    try:
        ast.parse(test_content)
        # It's valid now!
        with open(filepath, 'w') as f:
            f.write(test_content)
        print(f"Fixed {filepath}")
        return
    except SyntaxError:
        pass
        
    # If not, maybe it had multiple """ or we messed it up worse.
    print(f"Failed to fix {filepath}. Manual intervention may be needed.")

for root, dirs, files in os.walk('app'):
    for file in files:
        if file.endswith('.py'):
            fix_file(os.path.join(root, file))
