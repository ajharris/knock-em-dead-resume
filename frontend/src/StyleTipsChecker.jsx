import React, { useState } from "react";

const severityIcons = {
  info: "ℹ️",
  warning: "⚠️",
  critical: "❗"
};

export default function StyleTipsChecker({ resumeText }) {
  const [tips, setTips] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [resolved, setResolved] = useState([]);
  const [ignored, setIgnored] = useState([]);

  const checkStyle = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await fetch("/api/style_tips", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ resume_text: resumeText })
      });
      if (!res.ok) throw new Error("Failed to get style tips");
      const data = await res.json();
      setTips(data.tips || []);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const markResolved = idx => setResolved([...resolved, idx]);
  const markIgnored = idx => setIgnored([...ignored, idx]);

  return (
    <div style={{ margin: "2rem 0" }}>
      <button onClick={checkStyle} disabled={loading || !resumeText.trim()}>
        {loading ? "Checking..." : "Check Style"}
      </button>
      {error && <div style={{ color: "red" }}>{error}</div>}
      {tips.length > 0 && (
        <ul style={{ marginTop: 16 }} data-testid="tips-list">
          {tips.map((tip, i) => (
            <li
              key={i}
              data-testid={`tip-item-${i}`}
              style={{
                opacity: ignored.includes(i) ? 0.4 : 1,
                textDecoration: resolved.includes(i) ? "line-through" : "none",
                marginBottom: 8
              }}
            >
              <span style={{ marginRight: 8 }}>{severityIcons[tip.severity] || ""}</span>
              <span data-testid={`tip-text-${i}`}>{tip.tip}</span>
              <button onClick={() => markResolved(i)} style={{ marginLeft: 8 }} disabled={resolved.includes(i)}>
                Resolved
              </button>
              <button onClick={() => markIgnored(i)} style={{ marginLeft: 4 }} disabled={ignored.includes(i)}>
                Ignore
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
