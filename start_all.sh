#!/bin/bash
# Script to start both backend (FastAPI) and frontend (Vite) servers using concurrently



# Ensure frontend dependencies are installed only if needed
NPM_SENTINEL="frontend/node_modules/.built"
if [ ! -d frontend/node_modules ] || [ ! -f "$NPM_SENTINEL" ] || [ frontend/package.json -nt "$NPM_SENTINEL" ]; then
  echo "(Re)installing frontend dependencies..."
  npm install --prefix frontend
  touch "$NPM_SENTINEL"
else
  echo "Frontend dependencies are up to date."
fi

# Use npx to ensure local concurrently is used
npx concurrently \
  "bash -c '. venv/bin/activate && PYTHONPATH=backend uvicorn app.main:app --reload --host 0.0.0.0 --port 8000'" \
  "cd frontend && npm run dev"
