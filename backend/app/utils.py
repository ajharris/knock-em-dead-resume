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