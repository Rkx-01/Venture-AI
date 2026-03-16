import os

def fix_file(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
        
    in_docstring = False
    docstring_lines = []
    other_lines = []
    has_seen_future = False
    future_line = ""
    
    for line in lines:
        if line.startswith('from __future__ import annotations'):
            has_seen_future = True
            future_line = line
            continue
            
        if line.strip() == '"""' and not in_docstring and not docstring_lines:
            in_docstring = True
            docstring_lines.append(line)
        elif line.strip() == '"""' and in_docstring:
            in_docstring = False
            docstring_lines.append(line)
            continue
        elif in_docstring:
            docstring_lines.append(line)
        else:
            other_lines.append(line)
            
    if docstring_lines:
        new_content = ""
        if has_seen_future:
            new_content += future_line
        new_content += "".join(docstring_lines)
        new_content += '"""\n'
        new_content += "".join(other_lines)
        
        with open(filepath, 'w') as f:
            f.write(new_content)

for root, dirs, files in os.walk('app'):
    for file in files:
        if file.endswith('.py'):
            fix_file(os.path.join(root, file))
