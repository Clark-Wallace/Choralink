#!/usr/bin/env python3
"""
Choralink Requirements Checker
Helps new users verify their setup before running arrangements
"""

import sys
import importlib.util

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} is too old")
        print("   Choralink requires Python 3.8 or higher")
        print("   Please update your Python installation")
        return False
    else:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True

def check_package(package_name, import_name=None):
    """Check if a required package is installed"""
    if import_name is None:
        import_name = package_name
    
    spec = importlib.util.find_spec(import_name)
    if spec is None:
        print(f"❌ {package_name} is not installed")
        return False
    else:
        print(f"✅ {package_name} is installed")
        return True

def main():
    print("🎼 Choralink Requirements Check")
    print("=" * 35)
    
    # Check Python version
    python_ok = check_python_version()
    
    print("\nChecking required packages:")
    
    # List of required packages
    packages = [
        ("music21", "music21"),
        ("numpy", "numpy"),
        ("librosa", "librosa"),
    ]
    
    all_good = python_ok
    for package_name, import_name in packages:
        if not check_package(package_name, import_name):
            all_good = False
    
    print("\n" + "=" * 35)
    
    if all_good:
        print("🎉 All requirements satisfied!")
        print("You're ready to use Choralink!")
        print("\nTry this test command:")
        print("python3 backend/run_choralink.py --help")
    else:
        print("⚠️  Some requirements are missing")
        print("\nTo install missing packages, run:")
        print("pip3 install -r backend/requirements.txt")
        print("\nOr install individually:")
        for package_name, _ in packages:
            print(f"pip3 install {package_name}")
    
    return 0 if all_good else 1

if __name__ == "__main__":
    sys.exit(main())