#!/bin/bash
# Railway Deployment Verification Script
# Confirms Python 3.11 is being used

echo "=========================================="
echo "  Railway Python Version Verification"
echo "=========================================="
echo ""

echo "Python version:"
python3.11 --version || python3 --version || python --version

echo ""
echo "Python path:"
which python3.11 || which python3 || which python

echo ""
echo "Pip version:"
python3.11 -m pip --version || python3 -m pip --version || pip --version

echo ""
echo "asyncpg test import:"
python3.11 -c "import asyncpg; print(f'✓ asyncpg {asyncpg.__version__} loaded successfully')" 2>&1

echo ""
echo "=========================================="
echo "If you see Python 3.13.x above, this deployment will FAIL"
echo "If you see Python 3.11.x above, deployment should succeed"
echo "=========================================="
