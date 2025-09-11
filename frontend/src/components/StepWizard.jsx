import React, { useState } from 'react';
import StepSidebar from './StepSidebar';
import StepForm from './StepForm';
import TopBar from './TopBar';

const steps = [
  { title: 'Basic Info', required: true },
  { title: 'Career Direction', required: true },
  { title: 'Experience Summary', required: true },
  { title: 'Keywords', required: true },
  { title: 'Education', required: false },
  { title: 'Professional Affiliations', required: false },
  { title: 'Military Experience', required: false },
  { title: 'Publications/Presentations', required: false },
  { title: 'Patents/Copyright', required: false },
  { title: 'Computer Skills', required: false },
  { title: 'Languages', required: false },
  { title: 'Global Experience', required: false },
  { title: 'Awards', required: false },
  { title: 'Community/Volunteer', required: false },
  { title: 'Hobbies/Interests', required: false },
  { title: 'Achievements', required: true },
];

export default function StepWizard() {
  const [currentStep, setCurrentStep] = useState(0);
  const [completed, setCompleted] = useState(Array(steps.length).fill(false));

  const handleStepChange = (idx) => {
    if (completed[idx] || idx === currentStep) setCurrentStep(idx);
  };

  const handleComplete = () => {
    setCompleted((prev) => {
      const next = [...prev];
      next[currentStep] = true;
      return next;
    });
    if (currentStep < steps.length - 1) setCurrentStep(currentStep + 1);
  };

  const handleBack = () => {
    if (currentStep > 0) setCurrentStep(currentStep - 1);
  };

  const handleSkip = () => {
    if (!steps[currentStep].required && currentStep < steps.length - 1) setCurrentStep(currentStep + 1);
  };

  return (
    <div className="min-h-screen grid grid-cols-4 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100">
      <TopBar />
      <aside className="col-span-1 bg-gray-50 dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700">
        <StepSidebar steps={steps} currentStep={currentStep} completed={completed} onStepClick={setCurrentStep} />
      </aside>
      <main className="col-span-3 p-6">
        <StepForm
          step={steps[currentStep]}
          stepIndex={currentStep}
          onComplete={handleComplete}
          onBack={handleBack}
          onSkip={handleSkip}
          isFirst={currentStep === 0}
          isLast={currentStep === steps.length - 1}
        />
      </main>
    </div>
  );
}
