#!/bin/bash
# Script to start both backend (FastAPI) and frontend (Vite) servers using concurrently


# Ensure frontend dependencies are installed before starting
cd frontend && npm install && cd ..

# Use npx to ensure local concurrently is used
npx concurrently \
  "bash -c '. venv/bin/activate && PYTHONPATH=backend uvicorn app.main:app --reload --host 0.0.0.0 --port 8000'" \
  "cd frontend && npm run dev"
