import React, { useState } from "react";

const OAUTH_PROVIDERS = [
  {
    name: "Google",
    url: "/auth/google",
    icon: "🔵"
  },
  {
    name: "Facebook",
    url: "/auth/facebook",
    icon: "🔷"
  },
  {
    name: "LinkedIn",
    url: "/auth/linkedin/login",
    icon: "🔗"
  }
];

export default function OAuthButtons({ onLogin }) {
  const [error, setError] = useState(null);

  const handleOAuth = (provider) => {
    setError(null);
    // Open popup for OAuth
    const width = 500, height = 600;
    const left = window.screenX + (window.outerWidth - width) / 2;
    const top = window.screenY + (window.outerHeight - height) / 2;
    const popup = window.open(
      provider.url,
      "oauth_popup",
      `width=${width},height=${height},left=${left},top=${top}`
    );
    if (!popup) {
      setError("Popup blocked. Please allow popups and try again.");
      return;
    }
    // Listen for message from popup
    const listener = (event) => {
      if (event.origin !== window.location.origin) return;
      if (event.data.type === "oauth-success") {
        onLogin(event.data.user);
        popup.close();
        window.removeEventListener("message", listener);
      } else if (event.data.type === "oauth-error") {
        setError(event.data.error || "OAuth failed");
        popup.close();
        window.removeEventListener("message", listener);
      }
    };
    window.addEventListener("message", listener);
  };

  return (
    <div style={{ margin: "2rem 0" }}>
      <div style={{ display: "flex", gap: 16, justifyContent: "center" }}>
        {OAUTH_PROVIDERS.map((provider) => (
          <button
            key={provider.name}
            onClick={() => handleOAuth(provider)}
            style={{
              fontSize: 18,
              padding: "0.5rem 1.5rem",
              borderRadius: 6,
              border: "1px solid #ccc",
              background: "#fff",
              cursor: "pointer"
            }}
          >
            <span style={{ marginRight: 8 }}>{provider.icon}</span>
            Sign in with {provider.name}
          </button>
        ))}
      </div>
      {error && <div style={{ color: "red", marginTop: 12 }}>{error}</div>}
    </div>
  );
}
