import React from 'react';

export default function EditableAIField({ label, id, value, onChange, onSuggest, onRewrite, required, placeholder }) {
  return (
    <div className="mb-4">
      <label htmlFor={id} className="block font-medium mb-1" aria-required={required}>
        {label}
        {required && <span className="text-red-500 ml-1">*</span>}
      </label>
      <div className="flex gap-2">
        <textarea
          id={id}
          value={value}
          onChange={onChange}
          required={required}
          placeholder={placeholder}
          className="w-full rounded border border-gray-300 dark:border-gray-600 p-2 bg-white dark:bg-gray-900 focus:ring"
          aria-label={label}
        />
        {onSuggest && (
          <button type="button" onClick={onSuggest} aria-label="Suggest" className="px-2 py-1 rounded bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300 hover:bg-blue-200 dark:hover:bg-blue-800 focus:ring">Suggest</button>
        )}
        {onRewrite && (
          <button type="button" onClick={onRewrite} aria-label="Rewrite" className="px-2 py-1 rounded bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300 hover:bg-green-200 dark:hover:bg-green-800 focus:ring">Rewrite</button>
        )}
      </div>
    </div>
  );
}
