#!/bin/bash
# Script to start both backend (FastAPI) and frontend (Vite) servers using concurrently

concurrently \
	"cd backend/app && uvicorn main:app --reload --host 0.0.0.0 --port 8000" \
	"cd frontend && npm run dev"
