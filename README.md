# Setwise Inventory Manager

A Python-based webhook listener system for automatically adjusting inventory when Shopify set products are sold, canceled, or refunded.

## Local Dev

1. Copy `.env.example` to `.env` and fill in your credentials.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Start the FastAPI server:
   ```
   uvicorn src.main:app --reload
   ```
4. Start ngrok:
   ```
   ngrok http 8000
   ```
5. Use the ngrok HTTPS URL to register your Shopify webhooks.

## Deployment

- Deploys to [Railway](https://railway.app/)
