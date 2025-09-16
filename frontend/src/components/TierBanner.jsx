import React from "react";

export function TierBanner({ tier }) {
  return (
    <div style={{
      background: tier === "pro" ? "#d1e7dd" : "#fff3cd",
      color: tier === "pro" ? "#0f5132" : "#664d03",
      padding: "0.5rem 1rem",
      borderRadius: 6,
      marginBottom: 12,
      fontWeight: 600,
      textAlign: "center"
    }}>
      {tier === "pro"
        ? "Pro subscription allows booking with guaranteed availability."
        : "Public chargers are shown, availability not guaranteed."}
    </div>
  );
}
