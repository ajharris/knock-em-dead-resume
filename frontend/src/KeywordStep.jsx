import React, { useState } from "react";
import KeywordChips from "./KeywordChips";

export default function KeywordStep({ jobAdId, jobDescription, onKeywordsChange }) {
  const [keywords, setKeywords] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchKeywords = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("/extract_keywords", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ job_description: jobDescription })
      });
      console.log('fetchKeywords: response', res);
      if (!res.ok) throw new Error("Failed to extract keywords");
      const data = await res.json();
      console.log('fetchKeywords: data', data);
      setKeywords(data.keywords);
      onKeywordsChange && onKeywordsChange(data.keywords);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  React.useEffect(() => {
    if (jobDescription) fetchKeywords();
  }, [jobDescription]);

  return (
    <div>
      <h3>Extracted Keywords</h3>
      {loading && <div>Extracting keywords...</div>}
      {error && <div style={{ color: "red" }}>{error}</div>}
      <KeywordChips
        keywords={keywords}
        onChange={setKeywords}
        onRegenerate={fetchKeywords}
      />
      <div style={{ marginTop: 16, color: "#666" }}>
        Edit, add, or remove keywords as needed. Click Regenerate to re-run AI extraction.
      </div>
    </div>
  );
}
