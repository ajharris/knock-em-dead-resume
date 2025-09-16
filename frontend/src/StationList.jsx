import React from "react";
import { StationMarker } from "./components/StationMarker";
import { BookButton } from "./components/BookButton";

export default function StationList({ stations, tier, onBook }) {
  return (
    <div>
      {stations.map((station) => (
        <div key={station.id} style={{ display: "flex", alignItems: "center", marginBottom: 8, border: "1px solid #eee", borderRadius: 6, padding: 8 }}>
          <StationMarker station={station} />
          <div style={{ flex: 1, marginLeft: 12 }}>
            <div><b>{station.name}</b> ({station.type})</div>
            <div>{station.location}</div>
            {station.is_public === 0 && (
              <div style={{ fontSize: 12, color: "#888" }}>
                Host: {station.host_id} | Price: {station.price || "-"} | Rating: {station.rating || "-"}
              </div>
            )}
          </div>
          <BookButton tier={tier} onBook={() => onBook(station)} />
        </div>
      ))}
    </div>
  );
}
