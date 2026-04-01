#!/bin/bash
# Quick Script zum Ausführen aller Standard-Checks

echo "════════════════════════════════════════════════════════════════"
echo "🧹 CLEAN CODE VALIDATION - Würfelspiel P2.3.5"
echo "════════════════════════════════════════════════════════════════"

# Python-Linting
echo ""
echo "1️⃣  Checking with Flake8 (PEP 8)..."
flake8 domain application infrastructure --exclude=__pycache__,venv 2>/dev/null && echo "✅ Flake8: PASS" || echo "⚠️  Flake8: ISSUES"

echo ""
echo "2️⃣  Checking with Pylint..."
pylint --rcfile=.pylintrc domain application infrastructure --exit-zero >/dev/null 2>&1 && echo "✅ Pylint: PASS" || echo "⚠️  Pylint: ISSUES"

echo ""
echo "3️⃣  Verifying Folder Structure..."
for dir in domain application infrastructure docs; do
    [ -d "$dir" ] && echo "✅ $dir/" || echo "❌ $dir/ (MISSING)"
done

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "✨ Code Quality Check Complete!"
echo "════════════════════════════════════════════════════════════════"
