
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
  jest.restoreAllMocks();
});

test('calls backend and redirects to Stripe', async () => {
  const openMock = jest.spyOn(window, 'open').mockImplementation(() => {});

  render(<PaymentForm stationId={1} stationName="Test" price={10} userId={1} />);
  const btn = screen.getByText(/Pay \$10/);
  fireEvent.click(btn);

  await waitFor(() => {
    expect(openMock).toHaveBeenCalledWith('https://stripe.test/session', '_self');
  });

  openMock.mockRestore();
});
