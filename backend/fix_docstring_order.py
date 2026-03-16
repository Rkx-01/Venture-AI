import os
import glob
import subprocess

def fix_file(path):
    with open(path, 'r') as f:
        content = f.read()
        
    if "from __future__ import annotations" not in content:
        return
        
    # We want docstring first, then __future__, then everything else.
    # Split the file by lines.
    lines = content.split('\n')
    
    # Remove all future imports
    filtered_lines = [l for l in lines if l.strip() != "from __future__ import annotations"]
    
    # Find the end of the docstring if it's at the top 
    # (it might be the first thing now that future is gone)
    doc_end_idx = 0
    if len(filtered_lines) > 0 and filtered_lines[0].startswith('"""'):
        # It's a top-level docstring
        if filtered_lines[0] == '"""' or (filtered_lines[0].count('"""') == 1):
            # multi-line docstring
            for i in range(1, len(filtered_lines)):
                if '"""' in filtered_lines[i]:
                    doc_end_idx = i + 1
                    break
        else:
            # single-line docstring e.g. """doc"""
            doc_end_idx = 1
            
    # Insert the future import right after the docstring
    filtered_lines.insert(doc_end_idx, "from __future__ import annotations")
    
    # Also remove any extra blank lines before the future import if doc_end_idx == 0
    
    with open(path, 'w') as f:
        f.write('\n'.join(filtered_lines))

for root, _, files in os.walk('app'):
    for file in files:
        if file.endswith('.py'):
            fix_file(os.path.join(root, file))

print("Fixed docstring order. Running ruff fix...")
subprocess.run(["venv/bin/ruff", "check", "--fix", "app"])
