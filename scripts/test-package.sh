#!/bin/bash
# Test script to validate package installation (replicates CI environment)
# This ensures the package works correctly for end users

set -e  # Exit on error

echo "=========================================="
echo "Testing Package Installation (CI-like)"
echo "=========================================="
echo ""

# Get the project root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

# Detect Python - prefer system python over conda for package building
if command -v /usr/bin/python3 &> /dev/null; then
    PYTHON=/usr/bin/python3
    PIP=/usr/bin/python3
elif command -v python3 &> /dev/null; then
    PYTHON=python3
    PIP=python3
else
    echo "Error: python3 not found"
    exit 1
fi

echo "Using Python: $($PYTHON --version)"
echo ""

echo "1. Uninstalling existing editable installation..."
$PIP -m pip uninstall -y joblet-sdk-python 2>/dev/null || echo "   (no existing installation)"
echo ""

echo "2. Cleaning build artifacts..."
rm -rf build/ dist/ *.egg-info joblet_sdk_python.egg-info
echo "   ✓ Cleaned"
echo ""

echo "3. Building package..."
$PYTHON -m build --sdist --wheel
echo "   ✓ Built successfully"
echo ""

echo "4. Installing package from wheel (non-editable)..."
$PIP -m pip install dist/joblet_sdk_python-*.whl --force-reinstall
echo "   ✓ Installed"
echo ""

echo "5. Testing imports (from installed package)..."
cd /tmp  # Move out of source directory to ensure we're testing the installed package
$PYTHON -c "
from joblet import JobletClient
from joblet.proto import persist_pb2, persist_pb2_grpc
from joblet.services import JobService, PersistService
print('   ✓ All imports successful')
"
cd "$PROJECT_ROOT"
echo ""

echo "6. Running tests against installed package..."
$PYTHON -m pytest tests/ -v --tb=short
echo ""

echo "=========================================="
echo "✓ Package validation complete!"
echo "=========================================="
echo ""
echo "To restore editable install for development:"
echo "  pip uninstall joblet-sdk-python"
echo "  pip install -e ."
