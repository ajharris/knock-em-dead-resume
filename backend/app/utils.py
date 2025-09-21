def normalize_keywords(keywords: list[str]) -> list[str]:
    # Deduplicate, lowercase, but preserve domain capitalization (e.g., Python, SQL)
    seen = set()
    normalized = []
    for kw in keywords:
        kw_clean = kw.strip()
        # Preserve capitalization for known tech/skills
        if kw_clean.lower() in ["python", "sql", "aws", "excel", "javascript", "c++", "c#", "java", "linux", "docker", "kubernetes"]:
            norm = kw_clean.title() if kw_clean.islower() else kw_clean
        else:
            norm = kw_clean.lower()
        if norm not in seen:
            seen.add(norm)
            normalized.append(norm)
    return normalized

import io
from typing import BinaryIO
from pdfminer.high_level import extract_text as pdf_extract_text
from docx import Document
import re

def extract_text_from_file(file) -> str:
    filename = file.filename.lower()
    if filename.endswith('.pdf'):
        return extract_text_from_pdf(file)
    elif filename.endswith('.docx'):
        return extract_text_from_docx(file)
    elif filename.endswith('.txt'):
        return file.read().decode('utf-8')
    else:
        return ''

def extract_text_from_pdf(file: BinaryIO) -> str:
    file.seek(0)
    return pdf_extract_text(file)

def extract_text_from_docx(file: BinaryIO) -> str:
    file.seek(0)
    doc = Document(file)
    return '\n'.join([p.text for p in doc.paragraphs])

def extract_keywords(text: str) -> set:
    # Simple keyword extraction: words > 2 chars, ignore stopwords
    stopwords = set(['the','and','for','with','that','this','from','are','was','but','not','you','all','any','can','had','her','his','our','out','has','have','will','who','their','they','she','him','her','its','then','were','which','when','what','where','how','why','your','about','into','than','them','these','those','such','only','other','some','could','would','should','shall','may','might','must','each','every','either','neither','both','few','more','most','much','many','own','same','so','too','very','required'])
    words = re.findall(r'\b\w{3,}\b', text.lower())
    return set(w for w in words if w not in stopwords)

def compare_keywords(job_ad_text: str, resume_text: str) -> dict:
    job_keywords = extract_keywords(job_ad_text)
    resume_keywords = extract_keywords(resume_text)
    matches = sorted(list(job_keywords & resume_keywords))
    gaps = sorted(list(job_keywords - resume_keywords))
    summary = {
        'num_matches': len(matches),
        'num_gaps': len(gaps),
        'coverage': f"{len(matches)}/{len(job_keywords)}"
    }
    return {'matches': matches, 'gaps': gaps, 'summary': summary}