#!/bin/bash
# Build frontend and copy to backend/app/build for Heroku static serving
set -e
cd "$(dirname "$0")"
cd frontend
npm ci
npm run build
rm -rf ../backend/app/build
cp -r dist ../backend/app/build
