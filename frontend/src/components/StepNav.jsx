import React from 'react';

export default function StepNav({ onBack, onSkip, onComplete, isFirst, isLast, required }) {
  return (
    <nav className="flex justify-between mt-6" aria-label="Step navigation">
      <button
        type="button"
        onClick={onBack}
        disabled={isFirst}
        aria-label="Go to previous step"
        className={`px-4 py-2 rounded font-medium focus:ring ${isFirst ? 'bg-gray-200 dark:bg-gray-700 text-gray-500 dark:text-gray-300 cursor-not-allowed' : 'bg-white dark:bg-gray-900 text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700'}`}
      >
        Back
      </button>
      {!required && (
        <button
          type="button"
          onClick={onSkip}
          aria-label="Skip this step"
          className="px-4 py-2 rounded font-medium bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-300 hover:bg-yellow-200 dark:hover:bg-yellow-800 focus:ring"
        >
          Skip
        </button>
      )}
      <button
        type="button"
        onClick={onComplete}
        aria-label={isLast ? 'Finish resume' : 'Save and continue to next step'}
        className="px-4 py-2 rounded font-medium bg-blue-600 dark:bg-blue-500 text-white hover:bg-blue-700 dark:hover:bg-blue-400 focus:ring"
      >
        {isLast ? 'Finish' : 'Save & Continue'}
      </button>
    </nav>
  );
}
