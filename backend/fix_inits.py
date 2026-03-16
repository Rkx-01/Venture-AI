import os
import glob
for root, _, files in os.walk('app'):
    for f in files:
        if f == '__init__.py':
            path = os.path.join(root, f)
            with open(path, 'r') as fp: lines = fp.readlines()
            new_lines = [l for l in lines if "from typing import Optional, Any, List, Dict, Union, Tuple" not in l]
            with open(path, 'w') as fp: fp.writelines(new_lines)
