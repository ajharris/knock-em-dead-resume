import React, { useState } from "react";


import StepWizard from "./components/StepWizard";
import LandingPage from "./LandingPage";
import BulletRewriter from "./BulletRewriter";
import ResumeEditor from "./ResumeEditor";
import MyResumesDashboard from "./MyResumesDashboard";
import JobAdScanner from "./JobAdScanner";
import { TierBanner } from "./components/TierBanner";



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
    <div>
      <TierBanner tier={tier} />
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
