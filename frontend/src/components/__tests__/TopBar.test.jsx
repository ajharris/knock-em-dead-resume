import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import TopBar from '../TopBar';

describe('TopBar', () => {
  it('renders app title', () => {
    render(<TopBar />);
    expect(screen.getByText(/Knock 'Em Dead Resume/i)).toBeInTheDocument();
  });
  it('renders dark mode toggle and user menu', () => {
    render(<TopBar />);
    expect(screen.getByRole('button', { name: /Toggle dark mode/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /User menu/i })).toBeInTheDocument();
  });
  it('shows correct icon for dark/light mode', () => {
    render(<TopBar />);
    expect(screen.getByText('☀️')).toBeInTheDocument();
  });
});
