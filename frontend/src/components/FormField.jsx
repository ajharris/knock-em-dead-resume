import React from 'react';

export default function FormField({ label, id, children, required, ...props }) {
  return (
    <div className="mb-4">
      <label htmlFor={id} className="block font-medium mb-1" aria-required={required}>
        {label}
        {required && <span className="text-red-500 ml-1">*</span>}
      </label>
      {children}
    </div>
  );
}
