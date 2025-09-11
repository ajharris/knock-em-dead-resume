
import React, { useState } from "react";


import StepWizard from "./components/StepWizard";
import LandingPage from "./LandingPage";
import BulletRewriter from "./BulletRewriter";
import ResumeEditor from "./ResumeEditor";
import MyResumesDashboard from "./MyResumesDashboard";


function App() {
  const [started, setStarted] = useState(false);
  const [showDashboard, setShowDashboard] = useState(false);
  const [selectedResume, setSelectedResume] = useState(null);
  // TODO: Replace with real auth token logic
  const token = window.localStorage.getItem('token') || 'demo-token';

  const handleView = (resume) => {
    setSelectedResume({ ...resume, readOnly: true });
    setShowDashboard(false);
  };
  const handleEdit = (resume) => {
    setSelectedResume({ ...resume, readOnly: false });
    setShowDashboard(false);
  };

  return (
    <div>
      <button onClick={() => setShowDashboard((v) => !v)}>
        {showDashboard ? 'Hide' : 'Show'} My Resumes
      </button>
      {showDashboard && (
        <MyResumesDashboard
          token={token}
          onView={handleView}
          onEdit={handleEdit}
        />
      )}
      <ResumeEditor
        resume={selectedResume}
        onClose={() => setSelectedResume(null)}
        token={token}
      />
      <BulletRewriter />
  {started ? <StepWizard /> : <LandingPage onStart={() => setStarted(true)} />}
    </div>
  );
}


export default App;
