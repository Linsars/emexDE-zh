#!/usr/bin/env python3
import os, re

ui_strings = set()

for root, dirs, files in os.walk('.'):
    for f in files:
        if not f.endswith(('.swift', '.m', '.mm')):
            continue
        path = os.path.join(root, f)
        if '/.' in path or path.startswith('./.'):
            continue
        
        try:
            with open(path, 'r', errors='ignore') as fh:
                content = fh.read()
        except:
            continue
        
        # Pattern: title = "..." or text = "..." or message = "..."
        for m in re.finditer(r'(title|text|message|placeholder|prompt|label)\s*[:=]\s*"([^"]{2,80})"', content):
            ui_strings.add(m.group(2))
        
        # Pattern: Button("...")
        for m in re.finditer(r'Button\(\s*"([^"]{2,60})"\s*[,\)]', content):
            ui_strings.add(m.group(1))
        
        # Pattern: Text("...")
        for m in re.finditer(r'Text\(\s*"([^"]{2,120})"\s*\)', content):
            ui_strings.add(m.group(1))
        
        # Pattern: Label("...", systemImage:
        for m in re.finditer(r'Label\(\s*"([^"]{2,60})"\s*,', content):
            ui_strings.add(m.group(1))
        
        # Pattern: setTitle("..." forButton:
        for m in re.finditer(r'setTitle:\s*@"([^"]{2,80})"\s+forButton', content):
            ui_strings.add(m.group(1))
        
        # Pattern: alert with confirmTitle etc
        for m in re.finditer(r'confirmTitle:\s*@"([^"]+)"', content):
            ui_strings.add(m.group(1))
        
        # Pattern: self.title = "..." 
        for m in re.finditer(r'\.title\s*=\s*"([^"]{2,60})"', content):
            ui_strings.add(m.group(1))
        
        # Pattern: NotifyUser with notification string
        for m in re.finditer(r'notification:\s*@"([^"]{2,120})"', content):
            ui_strings.add(m.group(1))

print(f"Found {len(ui_strings)} user-facing strings")
for s in sorted(ui_strings):
    print(s)
