import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import StepWizard from '../StepWizard';

describe('StepWizard', () => {
  it('renders sidebar, top bar, and main content', () => {
    render(<StepWizard />);
    expect(screen.getByText(/Knock 'Em Dead Resume/i)).toBeInTheDocument();
    expect(screen.getByRole('navigation', { name: /Resume Steps/i })).toBeInTheDocument();
    expect(screen.getByRole('heading', { level: 2 })).toBeInTheDocument();
  });

  it('navigates steps with next and back', () => {
    render(<StepWizard />);
    const nextBtn = screen.getByRole('button', { name: /Save and continue to next step/i });
    fireEvent.click(nextBtn);
    expect(screen.getByText(/Step 2 of 16/)).toBeInTheDocument();
    const backBtn = screen.getByRole('button', { name: /Go to previous step/i });
    fireEvent.click(backBtn);
    expect(screen.getByText(/Step 1 of 16/)).toBeInTheDocument();
  });

  it('disables back on first step', () => {
    render(<StepWizard />);
    const backBtn = screen.getByRole('button', { name: /Go to previous step/i });
    expect(backBtn).toBeDisabled();
  });

  it('shows skip button for optional steps', () => {
    render(<StepWizard />);
    // Go to Education (step 5, index 4)
    let nextBtn;
    for (let i = 0; i < 4; i++) {
      nextBtn = screen.getByRole('button', { name: /Save and continue to next step/i });
      fireEvent.click(nextBtn);
    }
    expect(screen.getByRole('button', { name: /Skip this step/i })).toBeInTheDocument();
  });

  it('sidebar stepper is clickable for completed steps', () => {
    render(<StepWizard />);
    let nextBtn;
    for (let i = 0; i < 2; i++) {
      nextBtn = screen.getByRole('button', { name: /Save and continue to next step/i });
      fireEvent.click(nextBtn);
    }
    // Now step 1 is completed, click the first sidebar button (step 1)
    const sidebarBtns = screen.getAllByRole('button', { name: /Go to step 1/i });
    // The first occurrence is the completed step, the second is the current step (aria-current)
    fireEvent.click(sidebarBtns[0]);
    expect(screen.getByText(/Step 1 of 16/)).toBeInTheDocument();
  });

  it('has accessible labels and navigation', () => {
    render(<StepWizard />);
    expect(screen.getByRole('navigation', { name: /Resume Steps/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Save and continue to next step|Finish resume/i })).toBeInTheDocument();
  });
});
