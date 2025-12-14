import React, { useState } from "react";


import StepWizard from "./components/StepWizard";
import LandingPage from "./LandingPage";
import BulletRewriter from "./BulletRewriter";
import ResumeEditor from "./ResumeEditor";
import MyResumesDashboard from "./MyResumesDashboard";
import JobAdScanner from "./JobAdScanner";




function App() {
  const [started, setStarted] = useState(false);
  const [showDashboard, setShowDashboard] = useState(false);
  const [selectedResume, setSelectedResume] = useState(null);
  const [showScanner, setShowScanner] = useState(false);
  // TODO: Replace with real auth token logic
  const token = window.localStorage.getItem('token') || 'demo-token';
  // TODO: Replace with real user tier logic
  const tier = window.localStorage.getItem('tier') || 'free';

  const handleView = (resume) => {
    setSelectedResume({ ...resume, readOnly: true });
    setShowDashboard(false);
  };
  const handleEdit = (resume) => {
    setSelectedResume({ ...resume, readOnly: false });
    setShowDashboard(false);
  };

  return (
    <div style={{ maxWidth: "1200px", margin: "0 auto", padding: "0 1rem" }}>
      <div style={{background: '#ff0', color: '#000', padding: 8, marginBottom: 8}}>DEBUG: App component rendered</div>
      {/* <TierBanner tier={tier} /> removed: not part of project */}
      <div className="flex gap-2 mb-4">
        <button onClick={() => setShowDashboard((v) => !v)} className="bg-gray-200 px-3 py-1 rounded">
          {showDashboard ? 'Hide' : 'Show'} My Resumes
        </button>
        <button onClick={() => setShowScanner((v) => !v)} className="bg-blue-200 px-3 py-1 rounded">
          {showScanner ? 'Hide' : 'Show'} Job Ad Scanner
        </button>
      </div>
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
      {showScanner && <JobAdScanner />}
      {!showScanner && (started ? <StepWizard /> : <LandingPage onStart={() => setStarted(true)} />)}
    </div>
  );
}


export default App;
