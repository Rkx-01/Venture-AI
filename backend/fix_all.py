import subprocess

def fix_file(path):
    with open(path, 'r') as f:
        lines = f.readlines()
        
    # Check if docstring is at the top but AFTER imports
    # The actual easiest fix for E402 due to docstring:
    # move docstring to the absolute top, then from __future__, then the rest.
    
    # Actually, an even easier way is:
    pass

subprocess.run(["venv/bin/ruff", "check", "--fix", "."])
