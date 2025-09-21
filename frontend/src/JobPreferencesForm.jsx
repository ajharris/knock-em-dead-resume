import React, { useState } from "react";
import axios from "axios";
import API_BASE from "./services/apiBase";

export default function JobPreferencesForm({ userId, onComplete }) {
  const [form, setForm] = useState({
    relocate: "no",
    willing_to_travel: "no",
    job_title_1: "",
    job_title_2: "",
    job_title_3: "",
    desired_industry_segment: "",
    career_change: "no",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = e => {
    const { name, value } = e.target;
    setForm(f => ({ ...f, [name]: value }));
  };

  const handleSubmit = async e => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
  await axios.post(`${API_BASE}/profile/${userId}/job-preferences`, form);
      onComplete();
    } catch (err) {
      setError(err.response?.data?.detail || "Error saving job preferences");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: 12 }}>
      <label>
        Willing to Relocate?
        <select name="relocate" value={form.relocate} onChange={handleChange}>
          <option value="yes">Yes</option>
          <option value="no">No</option>
        </select>
      </label>
      <label>
        Willing to Travel?
        <select name="willing_to_travel" value={form.willing_to_travel} onChange={handleChange}>
          <option value="yes">Yes</option>
          <option value="no">No</option>
        </select>
      </label>
      <label>
        Top Job Title Choice 1
        <input name="job_title_1" value={form.job_title_1} onChange={handleChange} required />
      </label>
      <label>
        Top Job Title Choice 2
        <input name="job_title_2" value={form.job_title_2} onChange={handleChange} />
      </label>
      <label>
        Top Job Title Choice 3
        <input name="job_title_3" value={form.job_title_3} onChange={handleChange} />
      </label>
      <label>
        Desired Industry Segment
        <input name="desired_industry_segment" value={form.desired_industry_segment} onChange={handleChange} />
      </label>
      <label>
        Is this a career change?
        <select name="career_change" value={form.career_change} onChange={handleChange}>
          <option value="yes">Yes</option>
          <option value="no">No</option>
        </select>
      </label>
      {error && <div style={{ color: "red" }}>{error}</div>}
      <button type="submit" disabled={loading}>{loading ? "Saving..." : "Save & Continue"}</button>
    </form>
  );
}
