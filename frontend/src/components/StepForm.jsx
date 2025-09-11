import React from 'react';
import StepNav from './StepNav';

export default function StepForm({ step, stepIndex, onComplete, onBack, onSkip, isFirst, isLast }) {
  // TODO: Render step-specific form fields and AI helpers
  return (
    <section aria-labelledby="step-title" className="rounded-2xl shadow-md p-6 bg-white dark:bg-gray-800">
      <h2 id="step-title" className="text-2xl font-semibold mb-2">{step.title}</h2>
      <p className="mb-4 text-gray-600 dark:text-gray-300">Step {stepIndex + 1} of 16</p>
      {/* TODO: Step-specific form fields go here */}
      <div className="h-32 flex items-center justify-center text-gray-400 dark:text-gray-500">
        <span>Form fields for "{step.title}" coming soon…</span>
      </div>
      <StepNav
        onBack={onBack}
        onSkip={onSkip}
        onComplete={onComplete}
        isFirst={isFirst}
        isLast={isLast}
        required={step.required}
      />
    </section>
  );
}
