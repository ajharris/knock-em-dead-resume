#!/bin/bash
# Script to start both backend (FastAPI) and frontend (Vite) servers

# Start backend
cd app
nohup uvicorn main:app --reload --host 0.0.0.0 --port 8000 > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

echo "Backend started with PID $BACKEND_PID. Logs: backend.log"

# Start frontend
cd frontend
nohup npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

echo "Frontend started with PID $FRONTEND_PID. Logs: frontend.log"

echo "Both servers are running."
echo "Stop them with: kill $BACKEND_PID $FRONTEND_PID"
