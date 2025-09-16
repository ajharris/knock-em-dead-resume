import io
import pytest
from backend.api.scan_resume import scan_resume_bp
from backend.app.utils import extract_text_from_file
from flask import Flask

def create_test_app():
    app = Flask(__name__)
    app.register_blueprint(scan_resume_bp)
    return app

def test_scan_resume_endpoint(client):
    job_ad = (io.BytesIO(b"Python SQL AWS"), 'jobad.txt')
    resume = (io.BytesIO(b"Python SQL Java"), 'resume.txt')
    data = {
        'job_ad': job_ad,
        'resume': resume
    }
    response = client.post('/api/scan_resume', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'matches' in json_data
    assert 'gaps' in json_data
    assert 'summary' in json_data

@pytest.fixture
def client():
    app = create_test_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
