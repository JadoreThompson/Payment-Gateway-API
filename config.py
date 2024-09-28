import os
from dotenv import load_dotenv
import stripe


load_dotenv()

# Stripe Envs
STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")
stripe.api_key = STRIPE_API_KEY

STRIPE_PUBLIC_TEST_KEY = os.getenv('STRIPE_PUBLIC_TEST_KEY')
STRIPE_SECRET_TEST_KEY = os.getenv('STRIPE_SECRET_TEST_KEY')

STRIPE_BASE_URL = "https://api.stripe.com/v1/"
HEADER = {
    'Authorization': f'Bearer {STRIPE_SECRET_TEST_KEY}',
    'Content-Type': 'application/x-www-form-urlencoded'
}
