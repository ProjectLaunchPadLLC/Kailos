#!/usr/bin/env python3
"""
Kailos-Quantum Build Validation Script
Run this locally to validate the build before pushing.
"""

import os
import sys
import importlib.util
import subprocess

REQUIRED_FILES = [
    "core/llm.py",
    "memory/holographic.py",
    "visuals/dashboard.py",
    "main.py"
]

REQUIRED_DIRS = [
    "core",
    "memory",
    "visuals",
    "data"
]

def validate_structure(base_path="."):
    """Validate directory and file structure."""
    print("📁 Validating directory structure...")
    
    # Check directories
    for dir_name in REQUIRED_DIRS:
        dir_path = os.path.join(base_path, dir_name)
        if os.path.isdir(dir_path):
            print(f"  ✅ Directory exists: {dir_name}/")
        else:
            print(f"  ❌ Missing directory: {dir_name}/")
            return False
    
    # Check files
    for file_name in REQUIRED_FILES:
        file_path = os.path.join(base_path, file_name)
        if os.path.isfile(file_path):
            print(f"  ✅ File exists: {file_name}")
        else:
            print(f"  ❌ Missing file: {file_name}")
            return False
    
    return True

def validate_imports(base_path="."):
    """Validate that all modules can be imported."""
    print("\n📦 Validating module imports...")
    sys.path.insert(0, base_path)
    
    modules = [
        ("core.llm", "ResponseGenerator"),
        ("memory.holographic", "HolographicLattice"),
        ("visuals.dashboard", ["print_quantum_state", "visualize_heatmap", "dream_state"])
    ]
    
    success = True
    for module_name, components in modules:
        try:
            module = __import__(module_name, fromlist=[''])
            print(f"  ✅ Imported: {module_name}")
            
            if components:
                if isinstance(components, list):
                    for comp in components:
                        if hasattr(module, comp):
                            print(f"     ✅ Found: {comp}")
                        else:
                            print(f"     ❌ Missing: {comp}")
                            success = False
                else:
                    if hasattr(module, components):
                        print(f"     ✅ Found: {components}")
                    else:
                        print(f"     ❌ Missing: {components}")
                        success = False
        except Exception as e:
            print(f"  ❌ Failed to import {module_name}: {e}")
            success = False
    
    return success

def main():
    """Main validation function."""
    print("=" * 60)
    print(" KAILOS-QUANTUM BUILD VALIDATION")
    print("=" * 60)
    
    repo_path = "Repo" if os.path.isdir("Repo") else "."
    
    if validate_structure(repo_path):
        print("\n✅ Structure validation passed")
    else:
        print("\n❌ Structure validation failed")
        sys.exit(1)
    
    if validate_imports(repo_path):
        print("\n✅ Import validation passed")
    else:
        print("\n❌ Import validation failed")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ BUILD VALIDATION COMPLETE - SUCCESS")
    print("=" * 60)

if __name__ == "__main__":
    main()
