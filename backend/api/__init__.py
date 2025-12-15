# Bridge package so tests that import `backend.api.*` resolve
# to the actual implementation located at `backend/app/api/`.
import os
__path__.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app', 'api'))
