import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import StepNav from '../StepNav';

describe('StepNav', () => {
  it('renders Back, Skip, and Save & Continue buttons', () => {
    render(<StepNav onBack={() => {}} onSkip={() => {}} onComplete={() => {}} isFirst={false} isLast={false} required={false} />);
    expect(screen.getByRole('button', { name: /Go to previous step/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Skip this step/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Save and continue to next step/i })).toBeInTheDocument();
  });
  it('disables Back on first step', () => {
    render(<StepNav onBack={() => {}} onSkip={() => {}} onComplete={() => {}} isFirst={true} isLast={false} required={false} />);
    expect(screen.getByRole('button', { name: /Go to previous step/i })).toBeDisabled();
  });
  it('shows Finish on last step', () => {
    render(<StepNav onBack={() => {}} onSkip={() => {}} onComplete={() => {}} isFirst={false} isLast={true} required={false} />);
    expect(screen.getByRole('button', { name: /Finish resume/i })).toBeInTheDocument();
  });
  it('does not show Skip if required', () => {
    render(<StepNav onBack={() => {}} onSkip={() => {}} onComplete={() => {}} isFirst={false} isLast={false} required={true} />);
    expect(screen.queryByRole('button', { name: /Skip this step/i })).not.toBeInTheDocument();
  });
  it('calls handlers on click', () => {
    const onBack = jest.fn();
    const onSkip = jest.fn();
    const onComplete = jest.fn();
    render(<StepNav onBack={onBack} onSkip={onSkip} onComplete={onComplete} isFirst={false} isLast={false} required={false} />);
    fireEvent.click(screen.getByRole('button', { name: /Go to previous step/i }));
    fireEvent.click(screen.getByRole('button', { name: /Skip this step/i }));
    fireEvent.click(screen.getByRole('button', { name: /Save and continue to next step/i }));
    expect(onBack).toHaveBeenCalled();
    expect(onSkip).toHaveBeenCalled();
    expect(onComplete).toHaveBeenCalled();
  });
});
