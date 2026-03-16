import os
import subprocess

def fix_docstring_to_top(path):
    with open(path, 'r') as f:
        content = f.read()
        
    if '"""' not in content:
        return
        
    lines = content.split('\n')
    
    # Check if the docstring is already at the very top (unindented)
    if len(lines) > 0 and lines[0] == '"""':
        return

    doc_start_idx = -1
    doc_end_idx = -1
    for i, line in enumerate(lines[:20]): # Look in the first 20 lines
        # ONLY MATCH UNINDENTED DOCSTRINGS
        if line.startswith('"""') and doc_start_idx == -1:
            doc_start_idx = i
            if line.strip() == '"""' or line.count('"""') == 1:
                # multi-line docstring
                for j in range(i + 1, len(lines)):
                    if '"""' in lines[j]:
                        doc_end_idx = j
                        break
            else:
                # single line docstring
                doc_end_idx = i
            break
            
    if doc_start_idx == -1 or doc_end_idx == -1:
        return
        
    docstring_block = lines[doc_start_idx:doc_end_idx + 1]
    rest_of_lines = lines[:doc_start_idx] + lines[doc_end_idx + 1:]
    
    # Strip from __future__
    # Wait, if we keep from __future__ below the docstring, it works! No need to move it.
    
    new_lines = docstring_block + rest_of_lines
    
    with open(path, 'w') as f:
        f.write('\n'.join(new_lines))

for root, _, files in os.walk('app'):
    for file in files:
        if file.endswith('.py'):
            fix_docstring_to_top(os.path.join(root, file))

print("Fixed docstrings. Running ruff check and fix...")
subprocess.run(["venv/bin/ruff", "check", "--fix", "app"])
