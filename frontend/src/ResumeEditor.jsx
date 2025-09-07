import React, { useState } from "react";
import StyleTipsChecker from "./StyleTipsChecker";

export default function ResumeEditor() {
  const [resumeText, setResumeText] = useState("");

  return (
    <div style={{ maxWidth: 700, margin: "2rem auto", padding: 24, border: "1px solid #ddd", borderRadius: 8 }}>
      <h2>Resume Editor</h2>
      <textarea
        value={resumeText}
        onChange={e => setResumeText(e.target.value)}
        placeholder="Paste or write your resume here..."
        rows={12}
        style={{ width: "100%", fontFamily: "inherit", fontSize: 16 }}
      />
      <StyleTipsChecker resumeText={resumeText} />
    </div>
  );
}
