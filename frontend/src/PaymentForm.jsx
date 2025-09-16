import React from "react";

function PaymentForm({ stationId, stationName, price, userId }) {
  const handlePayment = async () => {
    const res = await fetch("/flask/api/create-checkout-session", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ stationId, stationName, price, userId })
    });
    const data = await res.json();
    if (data.url) {
      window.location.href = data.url;
    } else {
      alert("Payment failed to initialize");
    }
  };

  return (
    <button
      onClick={handlePayment}
      className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
    >
      Pay ${price}
    </button>
  );
}

export default PaymentForm;
