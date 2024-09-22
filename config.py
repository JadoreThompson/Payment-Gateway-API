import os
from dotenv import load_dotenv
import stripe


load_dotenv()

# Stripe Envs
STRIPE_PUBLIC_TEST_KEY = os.getenv('STRIPE_PUBLIC_TEST_KEY')
STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")
STRIPE_BASE_URL = "https://api.stripe.com/v1/"
stripe.api_key = STRIPE_API_KEY
