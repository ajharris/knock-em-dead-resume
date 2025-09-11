

import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import MyResumesDashboard from '../MyResumesDashboard';
import axios from 'axios';

jest.mock('axios');

const mockResumes = [
  { id: '1', title: 'Resume 1', updated_at: new Date().toISOString() },
  { id: '2', title: 'Resume 2', updated_at: new Date().toISOString() },
];

describe('MyResumesDashboard', () => {
  beforeEach(() => {
    axios.get.mockResolvedValue({ data: mockResumes });
  });
  afterEach(() => {
    jest.clearAllMocks();
  });

  it('renders resumes and actions', async () => {
    render(
      <MyResumesDashboard
        token="demo-token"
        onView={jest.fn()}
        onEdit={jest.fn()}
      />
    );
    expect(screen.getByText(/Loading/)).toBeInTheDocument();
    await waitFor(() => expect(screen.getByText('Resume 1')).toBeInTheDocument());
    expect(screen.getByText('Resume 2')).toBeInTheDocument();
    expect(screen.getAllByText('View').length).toBeGreaterThan(0);
    expect(screen.getAllByText('Edit').length).toBeGreaterThan(0);
    expect(screen.getAllByText('Delete').length).toBeGreaterThan(0);
    expect(screen.getAllByText('Duplicate').length).toBeGreaterThan(0);
    expect(screen.getAllByText('Rename').length).toBeGreaterThan(0);
  });

  it('calls onView and onEdit', async () => {
    const onView = jest.fn();
    const onEdit = jest.fn();
    render(
      <MyResumesDashboard
        token="demo-token"
        onView={onView}
        onEdit={onEdit}
      />
    );
    await waitFor(() => expect(screen.getByText('Resume 1')).toBeInTheDocument());
    fireEvent.click(screen.getAllByText('View')[0]);
    expect(onView).toHaveBeenCalled();
    fireEvent.click(screen.getAllByText('Edit')[0]);
    expect(onEdit).toHaveBeenCalled();
  });
});
