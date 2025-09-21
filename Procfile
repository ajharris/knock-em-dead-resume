release: alembic -c alembic.ini upgrade head
web: PYTHONPATH=backend uvicorn app.main:app --host=0.0.0.0 --port=${PORT}
