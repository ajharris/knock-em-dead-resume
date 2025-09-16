import { render, screen } from '@testing-library/react';
import PaymentSuccess from '../PaymentSuccess';

test('shows payment success message', () => {
  render(<PaymentSuccess />);
  expect(screen.getByText(/Payment Successful/i)).toBeInTheDocument();
});
