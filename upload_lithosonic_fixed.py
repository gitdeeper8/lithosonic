#!/usr/bin/env python3

"""LITHO-SONIC Upload v1.0.0 - نسخة مصححة"""

import requests
import hashlib
import os
import glob

TOKEN = "pypi-AgEIcHlwaS5vcmcCJGI2MmY5YTFjLTU5YzgtNGU1ZC1hNGY4LTFiNzllMWJiNjY0ZQACKlszLCJlZjQ3ZDllOS04YmU5LTQ2OWMtYWQ0OC0wODRhZTg4YzZjMTUiXQAABiDzgVt-_5PPOihyN1NnWuUHv17Suc9Y_FKVvHuRUPjwEA"

print("="*60)
print("🌍 LITHO-SONIC v1.0.0 Upload - PyPI")
print("="*60)

# قراءة README.md
with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()
print(f"📄 README.md: {len(readme)} حرف")

# البحث عن ملفات التوزيع
wheel_files = glob.glob("dist/*.whl")
tar_files = glob.glob("dist/*.tar.gz")

if not wheel_files and not tar_files:
    print("\n❌ لا توجد ملفات توزيع. جاري بناء الحزمة...")
    os.system("python -m build")
    
    # البحث مرة أخرى
    wheel_files = glob.glob("dist/*.whl")
    tar_files = glob.glob("dist/*.tar.gz")

print(f"\n📦 الملفات:")
for f in wheel_files + tar_files:
    print(f"   • {os.path.basename(f)}")

for filepath in wheel_files + tar_files:
    filename = os.path.basename(filepath)
    print(f"\n📤 رفع: {filename}")

    # تحديد نوع الملف
    if filename.endswith('.tar.gz'):
        filetype = 'sdist'
        pyversion = 'source'
    else:
        filetype = 'bdist_wheel'
        pyversion = 'py3'

    # حساب الهاشات
    with open(filepath, 'rb') as f:
        content = f.read()
    md5_hash = hashlib.md5(content).hexdigest()
    sha256_hash = hashlib.sha256(content).hexdigest()

    # بيانات الرفع (بدون requires_python)
    data = {
        ':action': 'file_upload',
        'metadata_version': '2.1',
        'name': 'lithosonic',
        'version': '1.0.0',
        'filetype': filetype,
        'pyversion': pyversion,
        'md5_digest': md5_hash,
        'sha256_digest': sha256_hash,
        'description': readme,
        'description_content_type': 'text/markdown',
        'author': 'Samir Baladi',
        'author_email': 'gitdeeper@gmail.com',
        'license': 'MIT',
        'summary': 'LITHO-SONIC: Lithospheric Resonance & Infrasonic Geomechanical Observatory',
        'home_page': 'https://lithosonic.netlify.app',
        'project_url': 'https://github.com/gitdeeper8/lithosonic',
        'keywords': 'geophysics, seismology, infrasound, biot-theory, acoustic-emission, fracture-mechanics, volcano-monitoring, earthquake-prediction, induced-seismicity'
    }

    # رفع الملف
    with open(filepath, 'rb') as f:
        response = requests.post(
            'https://upload.pypi.org/legacy/',
            files={'content': (filename, f, 'application/octet-stream')},
            data=data,
            auth=('__token__', TOKEN),
            timeout=60,
            headers={'User-Agent': 'LITHO-SONIC-Uploader/1.0'}
        )

    print(f"   الحالة: {response.status_code}")

    if response.status_code == 200:
        print("   ✅✅✅ نجاح!")
    else:
        print(f"   ❌ خطأ: {response.text[:200]}")

print("\n" + "="*60)
print("🔗 https://pypi.org/project/lithosonic/1.0.0/")
print("="*60)
