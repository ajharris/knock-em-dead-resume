release: alembic -c alembic.ini upgrade head
web: PYTHONPATH=backend gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:${PORT}
