import hmac
import hashlib
import base64
from fastapi import Request, HTTPException
from .config import SHOPIFY_WEBHOOK_SECRET

async def verify_shopify_webhook(request: Request):
    raw_body = await request.body()
    hmac_header = request.headers.get("X-Shopify-Hmac-Sha256")

    calculated_hmac = base64.b64encode(
        hmac.new(SHOPIFY_WEBHOOK_SECRET.encode('utf-8'), raw_body, hashlib.sha256).digest()
    ).decode()

    if not hmac.compare_digest(calculated_hmac, hmac_header):
        raise HTTPException(status_code=401, detail="Unauthorized webhook")
