import { render, fireEvent, screen } from '@testing-library/react';
import BulletRewriter from '../BulletRewriter';

describe('BulletRewriter', () => {
  it('renders input and button', () => {
    render(<BulletRewriter />);
    expect(screen.getByPlaceholderText(/Paste a job duty/i)).toBeInTheDocument();
    // Find all elements with 'Rewrite' and check for a button
    const rewriteButtons = screen.getAllByText(/Rewrite/);
    expect(rewriteButtons.some(el => el.tagName === 'BUTTON')).toBe(true);
  });

  it('shows error on failed rewrite', async () => {
    global.fetch = jest.fn(() => Promise.resolve({ ok: false }));
    render(<BulletRewriter />);
    fireEvent.change(screen.getByPlaceholderText(/Paste a job duty/i), { target: { value: 'foo' } });
    // Find all elements with 'Rewrite' and click the button
    const rewriteButtons = screen.getAllByText(/Rewrite/);
    const button = rewriteButtons.find(el => el.tagName === 'BUTTON');
    fireEvent.click(button);
    expect(await screen.findByText(/Failed to rewrite bullet/)).toBeInTheDocument();
  });
});
