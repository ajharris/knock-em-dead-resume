import React, { useState } from "react";

export default function KeywordChips({ keywords, onChange, onRegenerate }) {
  const [input, setInput] = useState("");
  const [chips, setChips] = useState(keywords || []);

  const addChip = (chip) => {
    if (chip && !chips.includes(chip)) {
      const newChips = [...chips, chip];
      setChips(newChips);
      onChange && onChange(newChips);
    }
  };

  const removeChip = (chip) => {
    const newChips = chips.filter((c) => c !== chip);
    setChips(newChips);
    onChange && onChange(newChips);
  };

  const handleInput = (e) => {
    setInput(e.target.value);
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && input.trim()) {
      addChip(input.trim());
      setInput("");
    }
  };

  return (
    <div>
      <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
        {chips.map((chip) => (
          <span key={chip} style={{ background: "#e0e0e0", borderRadius: 16, padding: "4px 12px", margin: 2, display: "inline-flex", alignItems: "center" }}>
            {chip}
            <button style={{ marginLeft: 6, background: "none", border: "none", cursor: "pointer" }} onClick={() => removeChip(chip)}>&times;</button>
          </span>
        ))}
        <input
          type="text"
          value={input}
          onChange={handleInput}
          onKeyDown={handleKeyDown}
          placeholder="Add keyword"
          style={{ border: "none", outline: "none", minWidth: 80 }}
        />
      </div>
      {onRegenerate && (
        <button style={{ marginTop: 8 }} onClick={onRegenerate}>Regenerate</button>
      )}
    </div>
  );
}
