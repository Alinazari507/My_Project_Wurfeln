#!/usr/bin/env python3
"""
Clean Code Linting Script für P2.3.5 Würfelspiel Projekt
Überprüft Code-Qualität und Standards aller Python-Dateien
"""

import os
import sys
import subprocess
from pathlib import Path


def run_command(cmd, description):
    """Führt Befehl aus und zeigt Ergebnis"""
    print(f"\n{'='*70}")
    print(f"🔍 {description}")
    print(f"{'='*70}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("⚠️  Warnungen:")
            print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return False


def main():
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    
    print("\n" + "🎯"*35)
    print("CLEAN CODE LINTING - P2.3.5 Würfelspiel")
    print("🎯"*35)
    
    results = {}
    
    # 1. Flake8 (PEP 8 Standards)
    if os.path.exists(".flake8"):
        results["Flake8 (PEP 8)"] = run_command(
            "flake8 domain application infrastructure --exclude=__pycache__,venv",
            "Flake8: PEP 8 Style Guide Überprüfung"
        )
    
    # 2. Pylint (Code-Qualität)
    if os.path.exists(".pylintrc"):
        results["Pylint (Code Quality)"] = run_command(
            "pylint --rcfile=.pylintrc domain application infrastructure --exit-zero",
            "Pylint: Code-Qualität und Best-Practices"
        )
    
    # 3. Files validieren
    print(f"\n{'='*70}")
    print(f"📂 Ordnerstruktur-Validierung")
    print(f"{'='*70}")
    
    required_dirs = ["domain", "application", "infrastructure", "docs"]
    for d in required_dirs:
        exists = "✅" if os.path.isdir(d) else "❌"
        print(f"{exists} {d}/")
    
    required_files = [".flake8", ".pylintrc"]
    for f in required_files:
        exists = "✅" if os.path.isfile(f) else "❌"
        print(f"{exists} {f}")
    
    # Summary
    print(f"\n{'='*70}")
    print("📊 ZUSAMMENFASSUNG")
    print(f"{'='*70}")
    
    for tool, passed in results.items():
        status = "✅ PASS" if passed else "⚠️  ISSUES GEFUNDEN"
        print(f"{status}: {tool}")
    
    print("\n" + "✨"*35)
    print("Clean Code Prüfung abgeschlossen!")
    print("✨"*35 + "\n")


if __name__ == "__main__":
    main()
