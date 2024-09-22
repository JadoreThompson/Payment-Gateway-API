import os
from dotenv import load_dotenv

load_dotenv()

STRIPE_API_KEY = os.getenv("STRIPE_PUBLIC_TEST_KEY")
STRIPE_BASE_URL = "https://api.stripe.com/v1/"
