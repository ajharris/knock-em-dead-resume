import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import ResumeEditor from '../ResumeEditor';

describe('ResumeEditor', () => {
  const resume = {
    id: '1',
    title: 'Test Resume',
    content: { summary: 'Test summary' },
    readOnly: false,
  };

  it('renders with title and content', () => {
    render(<ResumeEditor resume={resume} token="demo-token" onClose={jest.fn()} />);
    expect(screen.getByDisplayValue('Test Resume')).toBeInTheDocument();
    expect(screen.getByText('Resume Editor')).toBeInTheDocument();
    expect(screen.getByText('Save')).toBeInTheDocument();
    expect(screen.getByText('Save As New Version')).toBeInTheDocument();
  });

  it('calls onClose when Close is clicked', () => {
    const onClose = jest.fn();
    render(<ResumeEditor resume={resume} token="demo-token" onClose={onClose} />);
    fireEvent.click(screen.getByText('Close'));
    expect(onClose).toHaveBeenCalled();
  });

  it('shows Save As New Version dialog', () => {
    render(<ResumeEditor resume={resume} token="demo-token" onClose={jest.fn()} />);
    fireEvent.click(screen.getByText('Save As New Version'));
    // There are two elements with this text: the button and the dialog heading
    expect(screen.getAllByText('Save As New Version').length).toBeGreaterThan(1);
    expect(screen.getByPlaceholderText('New version title')).toBeInTheDocument();
  });
});
