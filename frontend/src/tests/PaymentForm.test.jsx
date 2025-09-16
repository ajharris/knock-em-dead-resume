import { render, screen, fireEvent } from '@testing-library/react';
import PaymentForm from '../PaymentForm';

global.fetch = jest.fn(() => Promise.resolve({
  json: () => Promise.resolve({ url: 'https://stripe.test/session' })
}));

test('calls backend and redirects to Stripe', async () => {
  delete window.location;
  window.location = { href: '' };
  render(<PaymentForm stationId={1} stationName="Test" price={10} userId={1} />);
  const btn = screen.getByText(/Pay \$10/);
  fireEvent.click(btn);
  // Wait for fetch and redirect
  await screen.findByText(/Pay \$10/);
  expect(window.location.href).toBe('https://stripe.test/session');
});
