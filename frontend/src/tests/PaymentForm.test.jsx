
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import PaymentForm from '../PaymentForm';

beforeEach(() => {
  global.fetch = jest.fn(() =>
    Promise.resolve({
      json: () => Promise.resolve({ url: 'https://stripe.test/session' }),
      clone: function () { return this; }
    })
  );
});

afterEach(() => {
  global.fetch.mockClear();
});

test('calls backend and redirects to Stripe', async () => {
  const assignMock = jest.fn();
  delete window.location;
  window.location = { assign: assignMock };

  render(<PaymentForm stationId={1} stationName="Test" price={10} userId={1} />);
  const btn = screen.getByText(/Pay \$10/);
  fireEvent.click(btn);

  await waitFor(() => {
    expect(assignMock).toHaveBeenCalledWith('https://stripe.test/session');
  });
});
