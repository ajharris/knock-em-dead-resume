import io
import pytest
from backend.app.utils import extract_text_from_file, extract_keywords, compare_keywords

def test_extract_keywords_basic():
    text = "Python, SQL, and AWS are required."
    keywords = extract_keywords(text)
    assert 'python' in keywords
    assert 'sql' in keywords
    assert 'aws' in keywords
    assert 'required' not in keywords

def test_compare_keywords_matches_and_gaps():
    job_ad = "Python, SQL, AWS, Docker"
    resume = "Python, SQL, Java"
    result = compare_keywords(job_ad, resume)
    assert set(result['matches']) == {'python', 'sql'}
    assert set(result['gaps']) == {'aws', 'docker'}
    assert result['summary']['num_matches'] == 2
    assert result['summary']['num_gaps'] == 2

def test_extract_text_from_txt():
    file = io.BytesIO(b"This is a test resume.")
    file.filename = 'resume.txt'
    text = extract_text_from_file(file)
    assert "test resume" in text
