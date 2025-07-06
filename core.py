import os
import subprocess
import time
import re
import importlib.util

IGNORED = ['core.py', 'requirements.txt']
RUNNING = {}

def extract_imports(file_path):
    imports = set()
    pattern = r'^\s*(import|from)\s+([a-zA-Z0-9_\.]+)'
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(pattern, line)
            if match:
                module = match.group(2).split('.')[0]
                if module not in ('os', 'sys', 'time', 'subprocess', 're'):  # built-ins
                    imports.add(module)
    return list(imports)

def is_installed(module):
    return importlib.util.find_spec(module) is not None

def install_missing(modules):
    for module in modules:
        if not is_installed(module):
            print(f"[📦] تثبيت المكتبة الناقصة: {module}")
            try:
                subprocess.check_call(['pip', 'install', module])
                with open("requirements.txt", "a", encoding="utf-8") as req:
                    req.write(f"{module}\n")
            except Exception as e:
                print(f"[❌] فشل التثبيت: {module} => {e}")

while True:
    for f in os.listdir('.'):
        if f.endswith('.py') and f not in IGNORED and f not in RUNNING:
            print(f"\n[✅] ملف جديد: {f}")
            # استخراج المكتبات ومحاولة تثبيتها
            try:
                required_modules = extract_imports(f)
                install_missing(required_modules)
            except Exception as e:
                print(f"[⚠️] خطأ في استخراج المكتبات: {e}")

            # تشغيل الملف
            try:
                process = subprocess.Popen(['python', f])
                RUNNING[f] = process
                print(f"[🚀] تم تشغيل: {f}")
            except Exception as e:
                print(f"[❌] فشل تشغيل: {f} => {e}")

    time.sleep(5)
