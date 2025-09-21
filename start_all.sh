#!/bin/bash
# Script to start both backend (FastAPI) and frontend (Vite) servers using concurrently

	concurrently \
		"bash -c '. venv/bin/activate && PYTHONPATH=backend uvicorn app.main:app --reload --host 0.0.0.0 --port 8000'" \
		"cd frontend && npm run dev"
