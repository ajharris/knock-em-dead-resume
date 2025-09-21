import os
import importlib

def test_openai_rewrite(monkeypatch):
    # Patch environment so ai_bullet_rewriter does not raise
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    # Reload module to pick up env var
    import backend.app.ai_bullet_rewriter as ai_bullet_rewriter
    def fake_openai(text):
        return [
            "Increased sales by 30% through targeted marketing initiatives.",
            "Reduced operational costs by $10,000 annually by streamlining workflows."
        ]
    monkeypatch.setattr(ai_bullet_rewriter, "rewrite_bullet_with_openai", fake_openai)
    bullets = ai_bullet_rewriter.rewrite_bullet_with_openai("Responsible for managing a team of engineers")
    assert len(bullets) == 2
    assert bullets[0].startswith("Increased")
