import React from 'react';

export default function KeywordList({ keywords, onAdd, onRemove }) {
  const [input, setInput] = React.useState('');

  const handleAdd = () => {
    if (input.trim()) {
      onAdd(input.trim());
      setInput('');
    }
  };

  return (
    <div className="mb-4">
      <label className="block font-medium mb-1">Keywords</label>
      <div className="flex flex-wrap gap-2 mb-2">
        {keywords.map((kw, idx) => (
          <span key={idx} className="inline-flex items-center px-2 py-1 rounded bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300">
            {kw}
            <button
              type="button"
              aria-label={`Remove keyword ${kw}`}
              className="ml-1 text-red-500 hover:text-red-700 focus:ring"
              onClick={() => onRemove(kw)}
            >
              ×
            </button>
          </span>
        ))}
      </div>
      <div className="flex gap-2">
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          className="rounded border border-gray-300 dark:border-gray-600 p-2 bg-white dark:bg-gray-900 focus:ring"
          aria-label="Add keyword"
          placeholder="Add keyword"
          onKeyDown={e => { if (e.key === 'Enter') { e.preventDefault(); handleAdd(); } }}
        />
        <button type="button" onClick={handleAdd} className="px-3 py-2 rounded bg-blue-600 dark:bg-blue-500 text-white hover:bg-blue-700 dark:hover:bg-blue-400 focus:ring" aria-label="Add keyword">Add</button>
      </div>
    </div>
  );
}
