#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validation script to ensure everything is ready for public release
"""
import os
import sys
from pathlib import Path
import subprocess
import json

def check_file_exists(file_path: str, description: str) -> bool:
    """Check if a file exists"""
    if Path(file_path).exists():
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ MISSING {description}: {file_path}")
        return False

def check_python_syntax(file_path: str) -> bool:
    """Check Python file syntax"""
    try:
        subprocess.run([sys.executable, "-m", "py_compile", file_path], 
                      check=True, capture_output=True)
        print(f"✅ Python syntax OK: {file_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Python syntax ERROR in {file_path}: {e}")
        return False

def check_yaml_syntax(file_path: str) -> bool:
    """Check YAML file syntax"""
    try:
        import yaml
        with open(file_path, 'r', encoding='utf-8') as f:
            yaml.safe_load(f)
        print(f"✅ YAML syntax OK: {file_path}")
        return True
    except Exception as e:
        print(f"❌ YAML syntax ERROR in {file_path}: {e}")
        return False

def check_json_syntax(file_path: str) -> bool:
    """Check JSON file syntax"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json.load(f)
        print(f"✅ JSON syntax OK: {file_path}")
        return True
    except Exception as e:
        print(f"❌ JSON syntax ERROR in {file_path}: {e}")
        return False

def main():
    """Main validation function"""
    print("🔍 Validating Auto Architecture Diagrams for public release...\n")
    
    errors = 0
    
    # Check required files
    required_files = [
        ("README.md", "Main documentation"),
        ("LICENSE", "License file"),
        ("SETUP.md", "Setup guide"),
        ("CONTRIBUTING.md", "Contributing guide"),
        ("CHANGELOG.md", "Changelog"),
        ("workflows/generate-diagram.yml", "Manual workflow"),
        ("workflows/generate-diagram-auto.yml", "Auto workflow"),
        (".github/workflows/test-scripts.yml", "Test workflow"),
        ("scripts/analyze_repo.py", "Repository analyzer"),
        ("scripts/ai_refiner.py", "AI refiner"),
        ("scripts/generate_architecture.py", "Architecture generator"),
        ("scripts/test_diagram.py", "Test script"),
        ("scripts/README.md", "Scripts documentation"),
        ("examples/requirements.txt", "Example requirements"),
        ("examples/sample-architecture.py", "Example architecture"),
        ("config/diagram-config.json", "Configuration example"),
    ]
    
    print("📁 Checking required files...")
    for file_path, description in required_files:
        if not check_file_exists(file_path, description):
            errors += 1
    
    print("\n🐍 Checking Python syntax...")
    python_files = [
        "scripts/analyze_repo.py",
        "scripts/ai_refiner.py", 
        "scripts/generate_architecture.py",
        "scripts/test_diagram.py",
        "examples/sample-architecture.py",
        "validate-release.py"
    ]
    
    for file_path in python_files:
        if Path(file_path).exists():
            if not check_python_syntax(file_path):
                errors += 1
    
    print("\n📄 Checking YAML syntax...")
    yaml_files = [
        "workflows/generate-diagram.yml",
        "workflows/generate-diagram-auto.yml",
        ".github/workflows/test-scripts.yml"
    ]
    
    for file_path in yaml_files:
        if Path(file_path).exists():
            if not check_yaml_syntax(file_path):
                errors += 1
    
    print("\n🔧 Checking JSON syntax...")
    json_files = [
        "config/diagram-config.json"
    ]
    
    for file_path in json_files:
        if Path(file_path).exists():
            if not check_json_syntax(file_path):
                errors += 1
    
    print("\n📊 Checking documentation completeness...")
    
    # Check README has essential sections
    readme_path = Path("README.md")
    if readme_path.exists():
        readme_content = readme_path.read_text(encoding='utf-8')
        required_sections = [
            "## ✨ Características",
            "## 🚀 Inicio Rápido", 
            "## 📁 Estructura del Proyecto",
            "## 🔧 Configuración",
            "## 🤖 Refinamiento con AI",
            "## 📊 Ejemplo de Diagrama",
            "## 🛠️ Workflows Disponibles",
            "## 🔍 Tecnologías Soportadas",
            "## 🚨 Solución de Problemas"
        ]
        
        for section in required_sections:
            if section in readme_content:
                print(f"✅ README section found: {section}")
            else:
                print(f"❌ README section MISSING: {section}")
                errors += 1
    
    # Final validation
    print(f"\n{'='*60}")
    if errors == 0:
        print("🎉 ✅ ALL VALIDATIONS PASSED!")
        print("🚀 Ready for public release!")
        print("\n📋 Next steps:")
        print("   1. Create GitHub repository")
        print("   2. Upload files")
        print("   3. Configure repository settings")
        print("   4. Test with a sample project")
        print("   5. Announce to the community!")
    else:
        print(f"❌ VALIDATION FAILED: {errors} error(s) found")
        print("🔧 Please fix the errors above before releasing")
        sys.exit(1)

if __name__ == "__main__":
    # Install yaml if not available
    try:
        import yaml
    except ImportError:
        print("Installing PyYAML for validation...")
        subprocess.run([sys.executable, "-m", "pip", "install", "PyYAML"], check=True)
        import yaml
    
    main()