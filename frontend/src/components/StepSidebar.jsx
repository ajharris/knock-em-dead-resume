import React from 'react';

export default function StepSidebar({ steps, currentStep, completed, onStepClick }) {
  return (
    <nav role="navigation" aria-label="Resume Steps" className="py-8">
      <ol className="space-y-2">
        {steps.map((step, idx) => (
          <li key={step.title}>
            <button
              type="button"
              className={`w-full flex items-center px-4 py-3 rounded-lg transition focus:outline-none focus:ring-2 focus:ring-blue-500 text-left
                ${idx === currentStep ? 'bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300 font-bold' :
                  completed[idx] ? 'text-green-600 dark:text-green-400' :
                  'hover:bg-gray-100 dark:hover:bg-gray-700'}
              `}
              aria-current={idx === currentStep ? 'step' : undefined}
              aria-label={`Go to step ${idx + 1}: ${step.title}`}
              onClick={() => onStepClick(idx)}
              tabIndex={0}
            >
              <span className="w-6 h-6 flex items-center justify-center mr-3 rounded-full border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700">
                {completed[idx] ? '✓' : idx + 1}
              </span>
              <span>{step.title}</span>
            </button>
          </li>
        ))}
      </ol>
    </nav>
  );
}
