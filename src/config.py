import os
from dotenv import load_dotenv

if os.getenv("RAILWAY_ENV") != "production":
    load_dotenv()

load_dotenv()

SHOP_URL = os.getenv("SHOP_URL")
SHOPIFY_ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")
SHOPIFY_WEBHOOK_SECRET = os.getenv("SHOPIFY_WEBHOOK_SECRET")
API_VERSION = os.getenv("API_VERSION", "2024-04")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
