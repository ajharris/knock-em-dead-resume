import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import StepSidebar from '../StepSidebar';

describe('StepSidebar', () => {
  const steps = [
    { title: 'Step 1', required: true },
    { title: 'Step 2', required: false },
    { title: 'Step 3', required: true },
  ];
  const completed = [true, false, false];
  it('renders all steps with correct labels', () => {
    render(<StepSidebar steps={steps} currentStep={0} completed={completed} onStepClick={() => {}} />);
    expect(screen.getByText('Step 1')).toBeInTheDocument();
    expect(screen.getByText('Step 2')).toBeInTheDocument();
    expect(screen.getByText('Step 3')).toBeInTheDocument();
  });
  it('shows checkmark for completed steps', () => {
    render(<StepSidebar steps={steps} currentStep={0} completed={completed} onStepClick={() => {}} />);
    expect(screen.getByText('✓')).toBeInTheDocument();
  });
  it('highlights current step', () => {
    render(<StepSidebar steps={steps} currentStep={1} completed={completed} onStepClick={() => {}} />);
    const btn = screen.getByRole('button', { name: /Go to step 2/i });
    expect(btn).toHaveClass('bg-blue-100');
  });
  it('calls onStepClick when a step is clicked', () => {
    const onStepClick = jest.fn();
    render(<StepSidebar steps={steps} currentStep={0} completed={completed} onStepClick={onStepClick} />);
    const btn = screen.getByRole('button', { name: /Go to step 2/i });
    fireEvent.click(btn);
    expect(onStepClick).toHaveBeenCalledWith(1);
  });
});
