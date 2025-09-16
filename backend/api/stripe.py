import os
import stripe
from flask import Blueprint, request, jsonify, current_app, abort
from backend.app.crud_patch_stripe import mark_booking_paid, mark_booking_failed

stripe_bp = Blueprint('stripe', __name__)

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@stripe_bp.route("/api/create-checkout-session", methods=["POST"])
def create_checkout_session():
    data = request.get_json()
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": f"Charging spot at {data.get('stationName', 'Unknown')}"},
                    "unit_amount": int(float(data["price"]) * 100),
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url="http://localhost:3000/payment-success",
            cancel_url="http://localhost:3000/payment-failure",
            metadata={
                "stationId": data.get("stationId"),
                "userId": data.get("userId"),
                "price": data.get("price"),
            }
        )
        return jsonify({"url": session.url})
    except Exception as e:
        return jsonify(error=str(e)), 400

@stripe_bp.route("/api/stripe/webhook", methods=["POST"])
def stripe_webhook():
    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    if event["type"] == "payment_intent.succeeded":
        intent = event["data"]["object"]
        # Use metadata to update booking status
        station_id = intent.get("metadata", {}).get("stationId")
        user_id = intent.get("metadata", {}).get("userId")
        mark_booking_paid(station_id, user_id)
    elif event["type"] == "payment_intent.payment_failed":
        intent = event["data"]["object"]
        station_id = intent.get("metadata", {}).get("stationId")
        user_id = intent.get("metadata", {}).get("userId")
        mark_booking_failed(station_id, user_id)
    return jsonify({"status": "success"})
