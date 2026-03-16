import os
import ast

def clean_docstrings(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    try:
        ast.parse(content)
        return
    except SyntaxError:
        pass

    with open(filepath, 'r') as f:
        lines = f.readlines()

    # Step 1: Remove ALL lines that are exactly '"""\n' or 'from __future__ import annotations'
    # at the very beginning of the file, up until we hit real content.
    
    cleaned_lines = []
    in_header = True
    has_future = False
    
    # We also want to remove loose '"""' from anywhere if they are causing syntax errors,
    # but that's risky. The main issue is at the top of the files.
    
    # Let's just fix the top
    while lines and lines[0].strip() in ('from __future__ import annotations', '"""'):
        line = lines.pop(0)
        if 'from __future__ import annotations' in line:
            has_future = True

    # Now the first line is the start of the docstring content
    # We need to add the """ before it.
    
    # Wait, where does the docstring end? It ends at the next '"""'
    # Let's find the first '"""' in the remaining lines.
    end_doc_idx = -1
    for i, line in enumerate(lines):
        if line.strip() == '"""':
            end_doc_idx = i
            break
            
    if end_doc_idx != -1:
        if has_future:
            lines.insert(0, 'from __future__ import annotations\n')
            lines.insert(1, '"""\n')
        else:
            lines.insert(0, '"""\n')
            
        test_content = "".join(lines)
        try:
            ast.parse(test_content)
            with open(filepath, 'w') as f:
                f.write(test_content)
            print(f"Fixed {filepath}")
            return
        except SyntaxError:
            pass
            
    # Fallback if the above didn't work. We might have broken docstrings inside functions.
    # We'll just print out the path so I can fix it manually.
    print(f"Could not automatically fix {filepath}")

for root, dirs, files in os.walk('app'):
    for file in files:
        if file.endswith('.py'):
            clean_docstrings(os.path.join(root, file))
