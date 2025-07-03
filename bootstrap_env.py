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
    # On Windows embed, python.exe is at top; on other OS, adjust accordingly
    if os.name == 'nt':
        return os.path.join(target_dir, 'python.exe')
    return shutil.which('python') or sys.executable


def main():
    root = os.getcwd()
    env_dir = os.path.join(root, '.venv')
    modules_dir = resource_path('modules')

    # 1) Determine host Python or fallback to embedded Python
    if os.name == 'nt':
        host_py = shutil.which('py') or shutil.which('python')
    else:
        host_py = shutil.which('python')

    if not host_py:
        embed_zip = os.path.join(modules_dir, 'python-embed.zip')
        if os.path.isfile(embed_zip):
            embed_dir = os.path.join(root, 'python_embedded')
            os.makedirs(embed_dir, exist_ok=True)
            print(f"Extracting embedded Python from {embed_zip} to {embed_dir}")
            host_py = extract_embedded_python(embed_zip, embed_dir)
        else:
            print("❌ No Python interpreter found and no embedded distribution. Please include python-embed.zip in modules.")
            sys.exit(1)

    # 2) Bootstrap pip into the host_python if provided
    get_pip = os.path.join(modules_dir, 'get-pip.py')
    if os.path.isfile(get_pip):
        run([host_py, get_pip, '--no-index', '--find-links', modules_dir])

    # 3) Create virtual environment if missing
    if not os.path.isdir(env_dir):
        run([host_py, '-m', 'venv', env_dir])

    # 4) Determine venv's python & pip
    if os.name == 'nt':
        venv_py = os.path.join(env_dir, 'Scripts', 'python.exe')
    else:
        venv_py = os.path.join(env_dir, 'bin', 'python')
    pip_cmd = [venv_py, '-m', 'pip']

    # 5) Upgrade pip in the venv
    run(pip_cmd + ['install', '--upgrade', 'pip'])

    # 6) Install each wheel in the embedded modules directory
    for fname in sorted(os.listdir(modules_dir)):
        if fname.lower().endswith('.whl'):
            wheel_path = os.path.join(modules_dir, fname)
            run(pip_cmd + ['install', '--no-index', wheel_path])

    # 7) Success message
    print("\n✅ Environment ready! Activate with:")
    if os.name == 'nt':
        print("   source .venv/Scripts/activate   (Git Bash)")
    else:
        print("   source .venv/bin/activate      (Linux/Mac)")

if __name__ == '__main__':
    main()
