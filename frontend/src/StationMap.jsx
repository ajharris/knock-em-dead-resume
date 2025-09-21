import React, { useEffect, useState } from "react";
import StationList from "./StationList";

export default function StationMap() {
  const [stations, setStations] = useState([]);
  const tier = window.localStorage.getItem('tier') || 'free';

  useEffect(() => {
  import("./services/apiBase").then(({ default: API_BASE }) => {
      fetch(`${API_BASE}/api/stations`, {
        headers: { Authorization: `Bearer ${window.localStorage.getItem('token')}` }
      })
        .then((r) => r.json())
        .then(setStations);
    });
  }, []);

  const handleBook = (station) => {
    if (tier === "free") {
      alert("Upgrade to Pro to book private chargers.");
      return;
    }
    // Booking logic here
    alert(`Booking station ${station.name}`);
  };

  return <StationList stations={stations} tier={tier} onBook={handleBook} />;
}
