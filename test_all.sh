#!/bin/bash
set -e

# Run from project root
cd "$(dirname "$0")"

# Backend: install and test
if [ -f requirements.txt ]; then
    echo "[Backend] Installing Python dependencies..."
    pip install -r requirements.txt
fi

if [ -d app ]; then
    echo "[Backend] Running pytest..."
    pytest --maxfail=1 --disable-warnings -v
fi

# Frontend: install and test
if [ -d frontend ]; then
    echo "[Frontend] Installing npm dependencies..."
    cd frontend
    npm install
    echo "[Frontend] Running Jest tests..."
    npx jest --passWithNoTests
    cd ..
fi

echo "All tests completed successfully."
