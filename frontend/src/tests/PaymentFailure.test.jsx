import { render, screen } from '@testing-library/react';
import PaymentFailure from '../PaymentFailure';

test('shows payment failure message', () => {
  render(<PaymentFailure />);
  expect(screen.getByText(/Payment Failed/i)).toBeInTheDocument();
});
