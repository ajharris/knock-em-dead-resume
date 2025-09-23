#!/bin/bash
# Run all backend and frontend tests for the project
set -e





# Backend: Only rebuild venv if requirements.txt or sentinel is newer/missing
PYTHON_BIN="python3.13"
if ! command -v $PYTHON_BIN &> /dev/null; then
  PYTHON_BIN="python3"
  echo "Warning: python3.13 not found, using $PYTHON_BIN instead."
fi

VENV_SENTINEL=".venv/.built"
if [ ! -d ".venv" ] || [ ! -f "$VENV_SENTINEL" ] || [ requirements.txt -nt "$VENV_SENTINEL" ]; then
  echo "(Re)building Python virtual environment..."
  rm -rf .venv
  $PYTHON_BIN -m venv .venv
  source .venv/bin/activate
  python --version
  pip install --upgrade pip
  pip install -r requirements.txt
  echo "Installed Python packages:"
  pip freeze
  touch "$VENV_SENTINEL"
else
  echo "Python venv is up to date."
  source .venv/bin/activate
fi


# Ensure DATABASE_URL uses postgresql:// scheme before backend tests
echo "Ensuring DATABASE_URL uses postgresql:// scheme..."
.venv/bin/python scripts/augment_env.py

# Ensure DATABASE_URL is set to a Postgres test DB (Heroku fallback)
# Load from .env if present
if [ -f .env ]; then
  set -o allexport
  source .env
  set +o allexport
fi
echo "DEBUG: DATABASE_URL is $DATABASE_URL"
if [[ -z "$DATABASE_URL" || "$DATABASE_URL" == sqlite* ]]; then
  echo "[run_all_tests.sh] Error: DATABASE_URL is not set or is using SQLite. Please set DATABASE_URL in your .env file to your Heroku Postgres URL."
  exit 2
fi

# Backend tests
if [ -d backend/tests ]; then
  echo "Running backend tests..."
  PYTHONPATH=$(pwd) .venv/bin/python -m pytest backend/tests
else
  echo "No backend tests found."
fi



# Frontend: Only run npm install if package.json or sentinel is newer/missing
if [ -d frontend/src/tests ]; then
  NPM_SENTINEL="frontend/node_modules/.built"
  if [ ! -d frontend/node_modules ] || [ ! -f "$NPM_SENTINEL" ] || [ frontend/package.json -nt "$NPM_SENTINEL" ]; then
    echo "(Re)installing frontend dependencies..."
    npm install --prefix frontend
    touch "$NPM_SENTINEL"
  else
    echo "Frontend dependencies are up to date."
  fi
  echo "Running frontend tests..."
  npm test --prefix frontend
else
  echo "No frontend tests found."
fi
