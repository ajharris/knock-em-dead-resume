import React from "react";

export function StationMarker({ station }) {
  const isPublic = station.is_public === 1;
  return (
    <div style={{
      display: "inline-block",
      padding: 6,
      borderRadius: "50%",
      background: isPublic ? "#1976d2" : "#ff9800",
      color: "white",
      fontWeight: 700,
      border: isPublic ? "2px solid #90caf9" : "2px solid #ffe0b2",
      margin: 2
    }}>
      {isPublic ? "P" : "PR"}
    </div>
  );
}
