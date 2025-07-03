#!/usr/bin/env python3
import sys
import os
import subprocess
import shutil
import zipfile


def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller bundle.
    """
    base_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    return os.path.join(base_path, relative_path)


def run(cmd):
    print(f"▶ {' '.join(cmd)}")
    subprocess.check_call(cmd)


def extract_embedded_python(zip_path, target_dir):
    """
    Extract an embeddable Python zip distribution to the target directory.
    """
    with zipfile.ZipFile(zip_path, 'r') as zf:
        zf.extractall(target_dir)
    return os.path.join(target_dir, 'python.exe') if os.name == 'nt' else os.path.join(target_dir, 'python')


def main():
    root = os.getcwd()
    env_dir = os.path.join(root, '.venv')
    modules_dir = resource_path('modules')

    # Determine host Python or fallback to embedded Python in modules
    if os.name == 'nt':
        host_py = shutil.which('py') or shutil.which('python')
    else:
        host_py = shutil.which('python')

    if not host_py:
        # Look for embeddable Python zip in modules
        embed_zip = os.path.join(modules_dir, 'python-embed.zip')
        if os.path.isfile(embed_zip):
            embed_dir = os.path.join(root, 'python_embedded')
            os.makedirs(embed_dir, exist_ok=True)
            print(f"Extracting embedded Python from {embed_zip} to {embed_dir}")
            host_py = extract_embedded_python(embed_zip, embed_dir)
        else:
            print("❌ No Python interpreter found and no embedded distribution. Please include python-embed.zip in modules.")
            sys.exit(1)

    # Create virtual environment if missing
    if not os.path.isdir(env_dir):
        run([host_py, '-m', 'venv', env_dir])

    # Determine venv's python
    venv_py = os.path.join(env_dir, 'Scripts' if os.name=='nt' else 'bin', 'python.exe' if os.name=='nt' else 'python')
    pip_cmd = [venv_py, '-m', 'pip']

    # Upgrade pip
    run(pip_cmd + ['install', '--upgrade', 'pip'])

    # Install each wheel in modules
    for fname in sorted(os.listdir(modules_dir)):
        if fname.lower().endswith('.whl'):
            wheel_path = os.path.join(modules_dir, fname)
            run(pip_cmd + ['install', '--no-index', wheel_path])

    print("\n✅ Environment ready! Activate with:")
    if os.name == 'nt':
        print("   source .venv/Scripts/activate   (Git Bash)")
    else:
        print("   source .venv/bin/activate      (Linux/Mac)")

if __name__ == '__main__':
    main()
