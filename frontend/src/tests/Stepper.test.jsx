import { render, screen } from '@testing-library/react';
import StepWizard from '../components/StepWizard';

describe('StepWizard', () => {
  it('renders sidebar and top bar', () => {
    render(<StepWizard />);
    expect(screen.getByRole('navigation', { name: /Resume Steps/i })).toBeInTheDocument();
    expect(screen.getByRole('heading', { level: 2 })).toBeInTheDocument();
  });
});
