#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify diagram generation works correctly
"""
import sys
from pathlib import Path

def test_diagram_generation():
    """Tests diagram generation"""
    print("🧪 Testing diagram generation...")
    
    # Verify architecture.py exists
    script_path = Path(__file__).parent / "architecture.py"
    if not script_path.exists():
        print(f"❌ ERROR: {script_path} does not exist")
        return False
    
    print(f"✅ architecture.py found: {script_path}")
    
    # Verify imports
    try:
        print("📦 Verifying imports...")
        import diagrams
        from diagrams import Diagram, Cluster, Edge
        print("✅ All imports OK")
    except ImportError as e:
        print(f"❌ ERROR in imports: {e}")
        print("   Install with: pip install diagrams")
        return False
    
    # Execute the script
    try:
        print("📊 Executing architecture.py...")
        exec(open(script_path).read())
        print("✅ Script executed without errors")
    except Exception as e:
        print(f"❌ ERROR executing script: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Verify PNG was generated
    png_files = list(script_path.parent.glob("*.png"))
    if png_files:
        png_file = png_files[0]
        print(f"✅ ✅ ✅ DIAGRAM GENERATED: {png_file}")
        print(f"   Size: {png_file.stat().st_size} bytes")
        return True
    else:
        print(f"❌ ERROR: No PNG file found")
        print(f"   Directory: {script_path.parent}")
        print(f"   Files in directory:")
        for f in script_path.parent.iterdir():
            print(f"     - {f.name}")
        return False

if __name__ == "__main__":
    success = test_diagram_generation()
    sys.exit(0 if success else 1)