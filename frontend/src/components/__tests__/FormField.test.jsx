import React from 'react';
import { render, screen } from '@testing-library/react';
import FormField from '../FormField';

describe('FormField', () => {
  it('renders label and children', () => {
    render(<FormField label="Name" id="name"><input id="name" /></FormField>);
    expect(screen.getByLabelText('Name')).toBeInTheDocument();
  });
  it('shows required asterisk', () => {
    render(<FormField label="Email" id="email" required><input id="email" /></FormField>);
    expect(screen.getByText('*')).toBeInTheDocument();
  });
});
