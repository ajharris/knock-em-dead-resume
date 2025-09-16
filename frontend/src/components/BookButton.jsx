import React from "react";

export function BookButton({ tier, onBook }) {
  if (tier === "free") {
    return (
      <button disabled style={{ background: "#eee", color: "#888", cursor: "not-allowed", padding: 8, borderRadius: 4 }}>
        Book (Pro only)
      </button>
    );
  }
  return (
    <button onClick={onBook} style={{ background: "#4caf50", color: "white", padding: 8, borderRadius: 4 }}>
      Book
    </button>
  );
}
