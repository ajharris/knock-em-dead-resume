import React from "react";

export default function LandingPage({ onStart }) {
  return (
    <div style={{ maxWidth: 600, margin: "4rem auto", padding: 32, border: "1px solid #ddd", borderRadius: 8, textAlign: "center" }}>
      <h1 style={{ fontSize: 32, marginBottom: 16 }}>Knock 'Em Dead Resume Builder</h1>
      <p style={{ fontSize: 18, marginBottom: 32 }}>
        Build a world-class resume step by step. Guided forms, smart suggestions, and AI-powered summaries help you stand out.
      </p>
      <button style={{ fontSize: 20, padding: "0.75rem 2rem", borderRadius: 6, background: "#007bff", color: "#fff", border: "none", cursor: "pointer" }} onClick={onStart}>
        Get Started
      </button>
    </div>
  );
}
