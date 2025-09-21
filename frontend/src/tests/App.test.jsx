import { render, screen } from '@testing-library/react';
import App from '../App';

describe('App', () => {
  it('renders TierBanner and BulletRewriter', () => {
    render(<App />);
    expect(screen.getByText(/AI Achievement Bullet Rewriter/i)).toBeInTheDocument();
  });
});
