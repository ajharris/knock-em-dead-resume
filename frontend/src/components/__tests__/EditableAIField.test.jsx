import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import EditableAIField from '../EditableAIField';

describe('EditableAIField', () => {
  it('renders label and textarea', () => {
    render(<EditableAIField label="Summary" id="summary" value="" onChange={() => {}} />);
    expect(screen.getByLabelText('Summary')).toBeInTheDocument();
  });
  it('shows Suggest and Rewrite buttons if handlers provided', () => {
    render(<EditableAIField label="Summary" id="summary" value="" onChange={() => {}} onSuggest={() => {}} onRewrite={() => {}} />);
    expect(screen.getByRole('button', { name: /Suggest/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Rewrite/i })).toBeInTheDocument();
  });
  it('calls handlers on click', () => {
    const onSuggest = jest.fn();
    const onRewrite = jest.fn();
    render(<EditableAIField label="Summary" id="summary" value="" onChange={() => {}} onSuggest={onSuggest} onRewrite={onRewrite} />);
    fireEvent.click(screen.getByRole('button', { name: /Suggest/i }));
    fireEvent.click(screen.getByRole('button', { name: /Rewrite/i }));
    expect(onSuggest).toHaveBeenCalled();
    expect(onRewrite).toHaveBeenCalled();
  });
});
