import { render, screen, fireEvent } from '@testing-library/react';
import JobPreferencesForm from './JobPreferencesForm';

describe('JobPreferencesForm', () => {
  it('renders all fields and submits data', async () => {
    const handleComplete = jest.fn();
    render(<JobPreferencesForm userId={1} onComplete={handleComplete} />);

    // Check all fields are present
    expect(screen.getByLabelText(/Willing to Relocate/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Willing to Travel/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Top Job Title Choice 1/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Desired Industry Segment/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Is this a career change/i)).toBeInTheDocument();

    // Fill required fields
    fireEvent.change(screen.getByLabelText(/Top Job Title Choice 1/i), { target: { value: 'Engineer' } });
    fireEvent.click(screen.getByText(/Save & Continue/i));

    // Should show loading state
    expect(screen.getByText(/Saving/i)).toBeInTheDocument();
  });
});
