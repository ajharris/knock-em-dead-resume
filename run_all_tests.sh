#!/bin/bash
# Run all backend and frontend tests for the project
set -e


# Backend tests
if [ -d backend/tests ]; then
  echo "Running backend tests..."
  PYTHONPATH=$(pwd) pytest backend/tests
else
  echo "No backend tests found."
fi

# Frontend tests
if [ -d frontend/src/tests ]; then
  echo "Running frontend tests..."
  npm test --prefix frontend
else
  echo "No frontend tests found."
fi
