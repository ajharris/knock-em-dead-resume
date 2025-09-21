import { render, fireEvent, screen } from '@testing-library/react';
import StyleTipsChecker from '../StyleTipsChecker';

describe('StyleTipsChecker', () => {
  it('renders check style button', () => {
    render(<StyleTipsChecker resumeText="foo" />);
    expect(screen.getByText(/Check Style/)).toBeInTheDocument();
  });
});
