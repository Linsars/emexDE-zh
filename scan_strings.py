#!/usr/bin/env python3
import os, re

strings_found = set()
file_strings = {}

for root, dirs, files in os.walk('.'):
    for f in files:
        if not f.endswith(('.swift', '.m', '.mm', '.h')):
            continue
        path = os.path.join(root, f)
        parts = path.split(os.sep)
        if any(p.startswith('.') for p in parts[:-1]):
            continue
        
        try:
            with open(path, 'r', errors='ignore') as fh:
                content = fh.read()
        except:
            continue
        
        matches = re.finditer(r'"([A-Za-z][A-Za-z0-9\s\-/:+()]+)"', content)
        for m in matches:
            s = m.group(1)
            if len(s) < 3 or len(s) > 80:
                continue
            if any(skip in s for skip in ['://', '//', '#{', '{', '}', '&=', 'com.', 'org.', 'app.', 'build/', '.xc', '.framework', 'file://', '.app', '.zip', '.png', '.json']):
                continue
            if s.startswith(('http', 'www', 'System/', 'usr/')):
                continue
            strings_found.add(s)
            if path not in file_strings:
                file_strings[path] = set()
            file_strings[path].add(s)

for s in sorted(strings_found):
    print(s)
