def extract_keywords_with_openai(text: str) -> list[str]:
    """
    Calls OpenAI API to extract keywords from a job description or resume text.
    Returns a list of keywords.
    """
    prompt = f"""
Extract the most important keywords (skills, technologies, certifications, job titles, etc.) from the following text. Return them as a Python list of strings.

Input: {text}

Output: Python list of keywords:
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert resume and job description analyzer."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=256,
        temperature=0.2,
    )
    content = response.choices[0].message.content.strip()
    # Try to eval the output as a Python list
    try:
        keywords = eval(content)
        if isinstance(keywords, list):
            return [str(k).strip() for k in keywords]
    except Exception:
        pass
    # Fallback: split by comma
    return [k.strip() for k in content.split(",") if k.strip()]
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not set in environment or .env file.")

# Debug: print all environment variables that might affect OpenAI
import sys
import inspect
print("[DEBUG] Environment variables relevant to OpenAI:")
for k, v in os.environ.items():
    if "OPENAI" in k or "PROXY" in k.upper():
        print(f"    {k}={v}")

# Debug: print OpenAI client signature
print("[DEBUG] OpenAI client signature:")
print(inspect.signature(OpenAI.__init__))

# Defensive wrapper for OpenAI client instantiation
try:
    client = OpenAI(api_key=OPENAI_API_KEY)
except TypeError as e:
    print("[DEFENSIVE WRAPPER] TypeError during OpenAI client instantiation:")
    print(e)
    import traceback
    traceback.print_exc()
    # Try to instantiate without any extra kwargs
    import inspect
    import sys
    # Print all local variables and their values
    print("[DEFENSIVE WRAPPER] Locals at error:", locals())
    # Exit to avoid further errors
    sys.exit(1)

def rewrite_bullet_with_openai(text: str) -> list[str]:
    """
    Calls OpenAI API to rewrite a job duty or weak resume bullet into 2-3 strong, achievement-oriented bullets.
    Returns a list of rewritten bullets.
    """
    prompt = f"""
Rewrite the following job duty or weak resume bullet into 2-3 strong, achievement-oriented resume bullets in the Knock 'Em Dead style. Each bullet should:
- Start with a strong action verb
- Quantify results (%, $, #, etc.) where possible
- Use the Challenge → Action → Result formula
- Be optimized for ATS (preserve keywords from the user's role/industry)

Input: {text}

Output: 2-3 achievement-oriented resume bullets:
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert resume writer."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=400,
        temperature=0.7,
    )
    content = response.choices[0].message.content.strip()
    # Split bullets (handle numbered, dash, or asterisk bullets)
    bullets = [line.strip("-* 0123456789.") for line in content.split("\n") if line.strip()]
    # Remove empty and short lines
    bullets = [b for b in bullets if len(b) > 20]
    return bullets[:3]  # Return up to 3
