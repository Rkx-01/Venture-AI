import os

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
        
    # The broken files have lines starting without quotes right at the top
    # Let's just find files that don't compile, and add """ at the start (after __future__)
    import ast
    try:
        ast.parse(content)
        return
    except SyntaxError:
        pass
        
    with open(filepath, 'r') as f:
        lines = f.readlines()
        
    if lines and lines[0].startswith('from __future__ import annotations'):
        lines.insert(1, '"""\n')
    else:
        lines.insert(0, '"""\n')
        
    with open(filepath, 'w') as f:
        f.write("".join(lines))

for root, dirs, files in os.walk('app'):
    for file in files:
        if file.endswith('.py'):
            fix_file(os.path.join(root, file))
