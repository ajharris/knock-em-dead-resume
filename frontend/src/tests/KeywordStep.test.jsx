import { render, screen } from '@testing-library/react';
import KeywordStep from '../KeywordStep';

describe('KeywordStep', () => {
  it('renders extracted keywords section', () => {
    render(<KeywordStep jobAdId={1} jobDescription="foo" onKeywordsChange={jest.fn()} />);
    expect(screen.getByText(/Extracted Keywords/i)).toBeInTheDocument();
  });
});
