import React from "react";

export default function PaymentFailure() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h1 className="text-3xl font-bold mb-4 text-red-600">Payment Failed</h1>
      <p className="text-lg">There was a problem processing your payment. Please try again or contact support.</p>
    </div>
  );
}
