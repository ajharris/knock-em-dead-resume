import React from 'react';

export default function TopBar() {
  return (
    <header className="sticky top-0 w-full h-14 bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700 flex items-center justify-between px-6 z-10">
      <div className="flex items-center space-x-2">
        <span className="font-bold text-lg">Knock 'Em Dead Resume</span>
      </div>
      <div className="flex items-center space-x-4">
        {/* TODO: User profile dropdown, settings, logout, dark mode toggle */}
        <button aria-label="Toggle dark mode" className="focus:ring rounded p-2">
          <span className="hidden dark:inline">🌙</span>
          <span className="dark:hidden">☀️</span>
        </button>
        <div className="relative">
          <button aria-label="User menu" className="focus:ring rounded-full bg-gray-200 dark:bg-gray-700 w-8 h-8 flex items-center justify-center">
            <span className="sr-only">Open user menu</span>
            <span>👤</span>
          </button>
          {/* TODO: Dropdown menu */}
        </div>
      </div>
    </header>
  );
}
