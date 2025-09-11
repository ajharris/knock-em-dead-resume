import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import KeywordList from '../KeywordList';

describe('KeywordList', () => {
  it('renders keywords and add input', () => {
    render(<KeywordList keywords={['python', 'sql']} onAdd={() => {}} onRemove={() => {}} />);
    expect(screen.getByText('python')).toBeInTheDocument();
    expect(screen.getByText('sql')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Add keyword')).toBeInTheDocument();
  });
  it('calls onAdd when Add button clicked', () => {
    const onAdd = jest.fn();
    render(<KeywordList keywords={[]} onAdd={onAdd} onRemove={() => {}} />);
    const input = screen.getByPlaceholderText('Add keyword');
    fireEvent.change(input, { target: { value: 'react' } });
    fireEvent.click(screen.getByRole('button', { name: /Add keyword/i }));
    expect(onAdd).toHaveBeenCalledWith('react');
  });
  it('calls onRemove when remove button clicked', () => {
    const onRemove = jest.fn();
    render(<KeywordList keywords={['js']} onAdd={() => {}} onRemove={onRemove} />);
    fireEvent.click(screen.getByRole('button', { name: /Remove keyword js/i }));
    expect(onRemove).toHaveBeenCalledWith('js');
  });
});
