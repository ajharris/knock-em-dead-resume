
import React, { useState } from "react";
import OAuthButtons from "./components/OAuthButtons";

export default function LandingPage({ onStart }) {
  const [user, setUser] = useState(null);
  return (
    <div style={{ maxWidth: 600, margin: "4rem auto", padding: 32, border: "1px solid #ddd", borderRadius: 8, textAlign: "center" }}>
      <h1 style={{ fontSize: 32, marginBottom: 16 }}>Knock 'Em Dead Resume Builder</h1>
      <p style={{ fontSize: 18, marginBottom: 32 }}>
        Build a world-class resume step by step. Guided forms, smart suggestions, and AI-powered summaries help you stand out.
      </p>
      {!user && <OAuthButtons onLogin={setUser} />}
      {user && (
        <div style={{ margin: "2rem 0" }}>
          <img src={user.avatar} alt="avatar" style={{ width: 64, height: 64, borderRadius: "50%", marginBottom: 8 }} />
          <div style={{ fontWeight: 600, fontSize: 20 }}>{user.name}</div>
          <div style={{ color: "#555" }}>{user.email}</div>
          <button style={{ marginTop: 16, fontSize: 18, padding: "0.5rem 2rem", borderRadius: 6, background: "#007bff", color: "#fff", border: "none", cursor: "pointer" }} onClick={onStart}>
            Continue
          </button>
        </div>
      )}
    </div>
  );
}
