import { render, fireEvent, screen } from '@testing-library/react';
import JobPreferencesForm from '../JobPreferencesForm';
import axios from 'axios';

describe('JobPreferencesForm', () => {
  it('renders all fields', () => {
    render(<JobPreferencesForm userId="1" onComplete={jest.fn()} />);
    expect(screen.getByLabelText(/Willing to Relocate/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Willing to Travel/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Top Job Title Choice 1/i)).toBeInTheDocument();
  });

  it('shows error on failed submit', async () => {
    jest.spyOn(axios, 'post').mockRejectedValue(new Error('fail'));
    render(<JobPreferencesForm userId="1" onComplete={jest.fn()} />);
    fireEvent.change(screen.getByLabelText(/Top Job Title Choice 1/i), { target: { value: 'Engineer' } });
    fireEvent.click(screen.getByText(/Save & Continue/));
    expect(await screen.findByText(/Error saving job preferences/)).toBeInTheDocument();
    axios.post.mockRestore();
  });
});
