from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from backend.app.utils import extract_text_from_file, compare_keywords

scan_resume_bp = Blueprint('scan_resume', __name__)

@scan_resume_bp.route('/api/scan_resume', methods=['POST'])
def scan_resume():
    if 'job_ad' not in request.files or 'resume' not in request.files:
        return jsonify({'error': 'Both job ad and resume files are required.'}), 400

    job_ad_file = request.files['job_ad']
    resume_file = request.files['resume']

    job_ad_text = extract_text_from_file(job_ad_file)
    resume_text = extract_text_from_file(resume_file)

    if not job_ad_text or not resume_text:
        return jsonify({'error': 'Failed to extract text from one or both files.'}), 400

    comparison = compare_keywords(job_ad_text, resume_text)

    return jsonify({
        'job_ad_text': job_ad_text,
        'resume_text': resume_text,
        'matches': comparison['matches'],
        'gaps': comparison['gaps'],
        'summary': comparison['summary']
    })
