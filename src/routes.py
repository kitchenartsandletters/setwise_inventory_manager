from fastapi import APIRouter, Request
from .utils import verify_shopify_webhook

router = APIRouter()

@router.post("/webhook")
async def receive_webhook(request: Request):
    await verify_shopify_webhook(request)
    payload = await request.json()
    print("✅ Webhook received:", payload)
    return {"status": "ok"}
