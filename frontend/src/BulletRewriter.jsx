import React, { useState } from "react";

export default function BulletRewriter() {
  const [input, setInput] = useState("");
  const [bullets, setBullets] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [used, setUsed] = useState(null);

  const handleRewrite = async () => {
    setLoading(true);
    setError("");
    setUsed(null);
    try {
  const API_BASE = (await import("./services/apiBase")).default;
      const res = await fetch(`${API_BASE}/api/rewrite_bullet`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: input }),
      });
      if (!res.ok) throw new Error("Failed to rewrite bullet");
      const data = await res.json();
      setBullets(data.bullets || []);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = (text) => {
    navigator.clipboard.writeText(text);
  };

  return (
    <div className="bullet-rewriter">
      <h2>AI Achievement Bullet Rewriter</h2>
      <textarea
        value={input}
        onChange={e => setInput(e.target.value)}
        placeholder="Paste a job duty or weak resume bullet..."
        rows={4}
        style={{ width: "100%" }}
      />
      <button onClick={handleRewrite} disabled={loading || !input.trim()}>
        {loading ? "Rewriting..." : "Rewrite"}
      </button>
      {error && <div style={{ color: "red" }}>{error}</div>}
      {bullets.length > 0 && (
        <div className="rewritten-bullets">
          <h3>Suggested Bullets</h3>
          <ul>
            {bullets.map((b, i) => (
              <li key={i} style={{ marginBottom: 8 }}>
                <span>{b}</span>
                <button onClick={() => handleCopy(b)} style={{ marginLeft: 8 }}>
                  Copy
                </button>
                <button onClick={() => setUsed(i)} style={{ marginLeft: 4 }}>
                  Use this
                </button>
                {used === i && <span style={{ color: "green", marginLeft: 8 }}>✔ Used</span>}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
