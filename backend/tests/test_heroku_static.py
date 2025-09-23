import os
import tempfile
import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_health_check():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_serve_react_index(monkeypatch):
    # Simulate React build directory and index.html
    with tempfile.TemporaryDirectory() as tmpdir:
        build_dir = os.path.join(tmpdir, "build")
        static_dir = os.path.join(build_dir, "static")
        os.makedirs(static_dir)
        index_path = os.path.join(build_dir, "index.html")
        with open(index_path, "w") as f:
            f.write("<html><body>React App</body></html>")
        # Patch the frontend_build_dir in app
        monkeypatch.setattr("backend.app.main.frontend_build_dir", build_dir)
        resp = client.get("/")
        assert resp.status_code == 200
        assert b"React App" in resp.content


def test_serve_static_file(monkeypatch):
    with tempfile.TemporaryDirectory() as tmpdir:
        build_dir = os.path.join(tmpdir, "build")
        static_dir = os.path.join(build_dir, "static")
        os.makedirs(static_dir)
        js_path = os.path.join(static_dir, "main.js")
        with open(js_path, "w") as f:
            f.write("console.log('hello');")
        index_path = os.path.join(build_dir, "index.html")
        with open(index_path, "w") as f:
            f.write("<html></html>")
        monkeypatch.setattr("backend.app.main.frontend_build_dir", build_dir)
        resp = client.get("/static/main.js")
        assert resp.status_code == 200
        assert b"hello" in resp.content


def test_fallback_to_index(monkeypatch):
    with tempfile.TemporaryDirectory() as tmpdir:
        build_dir = os.path.join(tmpdir, "build")
        os.makedirs(build_dir)
        index_path = os.path.join(build_dir, "index.html")
        with open(index_path, "w") as f:
            f.write("<html>SPA</html>")
        monkeypatch.setattr("backend.app.main.frontend_build_dir", build_dir)
        resp = client.get("/some/route")
        assert resp.status_code == 200
        assert b"SPA" in resp.content
