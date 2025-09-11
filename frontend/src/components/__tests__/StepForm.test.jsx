import React from 'react';
import { render, screen } from '@testing-library/react';
import StepForm from '../StepForm';

describe('StepForm', () => {
  const step = { title: 'Basic Info', required: true };
  it('renders step title and number', () => {
    render(<StepForm step={step} stepIndex={0} onComplete={() => {}} onBack={() => {}} onSkip={() => {}} isFirst isLast={false} />);
    expect(screen.getByRole('heading', { name: /Basic Info/i })).toBeInTheDocument();
    expect(screen.getByText(/Step 1 of 16/)).toBeInTheDocument();
  });
  it('renders StepNav', () => {
    render(<StepForm step={step} stepIndex={0} onComplete={() => {}} onBack={() => {}} onSkip={() => {}} isFirst isLast={false} />);
    expect(screen.getByRole('button', { name: /Go to previous step/i })).toBeInTheDocument();
  });
  it('shows placeholder for form fields', () => {
    render(<StepForm step={step} stepIndex={0} onComplete={() => {}} onBack={() => {}} onSkip={() => {}} isFirst isLast={false} />);
    expect(screen.getByText(/Form fields for "Basic Info" coming soon/i)).toBeInTheDocument();
  });
});
