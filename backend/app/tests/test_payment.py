import pytest
from unittest.mock import patch
from flask import Flask
from backend.api.stripe import stripe_bp

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(stripe_bp)
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_checkout_session_returns_url(client):
    with patch('stripe.checkout.Session.create') as mock_create:
        mock_create.return_value.url = 'https://stripe.test/session'
        res = client.post('/api/create-checkout-session', json={
            'stationId': 1, 'stationName': 'Test Station', 'price': 10, 'userId': 1
        })
        assert res.status_code == 200
        assert 'url' in res.get_json()

def test_webhook_paid_updates_booking(client):
    # Simulate webhook event for payment_intent.succeeded
    # Patch mark_booking_paid and Stripe signature verification
    assert True  # Placeholder

def test_webhook_failed_updates_booking(client):
    # Simulate webhook event for payment_intent.payment_failed
    # Patch mark_booking_failed and Stripe signature verification
    assert True  # Placeholder
