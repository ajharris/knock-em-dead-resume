import React, { useState, useEffect } from "react";
import StyleTipsChecker from "./StyleTipsChecker";
import { updateResume, duplicateResume } from "./services/resumeApi";

export default function ResumeEditor({ resume, onClose, token }) {
  const [resumeText, setResumeText] = useState("");
  const [title, setTitle] = useState("");
  const [readOnly, setReadOnly] = useState(false);
  const [showSaveAs, setShowSaveAs] = useState(false);
  const [saveAsTitle, setSaveAsTitle] = useState("");

  useEffect(() => {
    if (resume) {
      setResumeText(resume.content ? JSON.stringify(resume.content, null, 2) : "");
      setTitle(resume.title || "");
      setReadOnly(!!resume.readOnly);
    } else {
      setResumeText("");
      setTitle("");
      setReadOnly(false);
    }
  }, [resume]);

  const handleSave = async () => {
    if (!resume || !resume.id) return;
    await updateResume(resume.id, { title, content: JSON.parse(resumeText) }, token);
    alert("Resume updated!");
    if (onClose) onClose();
  };

  const handleSaveAs = async () => {
    await duplicateResume({ ...resume, title: saveAsTitle, content: JSON.parse(resumeText) }, token);
    alert("Saved as new version!");
    setShowSaveAs(false);
    if (onClose) onClose();
  };

  if (!resume) return null;

  return (
    <div style={{ maxWidth: 700, margin: "2rem auto", padding: 24, border: "1px solid #ddd", borderRadius: 8 }}>
      <h2>Resume Editor</h2>
      <label>
        Title:
        <input value={title} onChange={e => setTitle(e.target.value)} disabled={readOnly} style={{ width: "100%", fontSize: 16, marginBottom: 8 }} />
      </label>
      <textarea
        value={resumeText}
        onChange={e => setResumeText(e.target.value)}
        placeholder="Paste or write your resume here..."
        rows={12}
        style={{ width: "100%", fontFamily: "inherit", fontSize: 16 }}
        disabled={readOnly}
      />
      <StyleTipsChecker resumeText={resumeText} />
      <div style={{ marginTop: 16 }}>
        {!readOnly && (
          <>
            <button onClick={handleSave}>Save</button>
            <button onClick={() => setShowSaveAs(true)}>Save As New Version</button>
          </>
        )}
        <button onClick={onClose} style={{ marginLeft: 8 }}>Close</button>
      </div>
      {showSaveAs && (
        <div style={{ marginTop: 16, background: '#f9f9f9', padding: 12, borderRadius: 4 }}>
          <h4>Save As New Version</h4>
          <input value={saveAsTitle} onChange={e => setSaveAsTitle(e.target.value)} placeholder="New version title" style={{ width: '100%' }} />
          <button onClick={handleSaveAs} style={{ marginTop: 8 }}>Save</button>
          <button onClick={() => setShowSaveAs(false)} style={{ marginLeft: 8 }}>Cancel</button>
        </div>
      )}
    </div>
  );
}
