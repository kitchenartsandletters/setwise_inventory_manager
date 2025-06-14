import httpx
from .config import SHOP_URL, SHOPIFY_ACCESS_TOKEN, API_VERSION

headers = {
    "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

async def get_product_by_handle(handle: str):
    url = f"https://{SHOP_URL}/admin/api/{API_VERSION}/products.json?handle={handle}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        products = response.json().get("products", [])
        return products[0] if products else None

async def get_inventory_item_id(product: dict):
    if not product:
        return None
    variant = product.get("variants", [{}])[0]
    return variant.get("inventory_item_id")

async def get_location_id():
    # Hardcoded real inventory location ID
    return 40052293765

async def adjust_inventory(inventory_item_id: int, location_id: int, adjustment: int):
    url = f"https://{SHOP_URL}/admin/api/{API_VERSION}/inventory_levels/adjust.json"
    payload = {
        "inventory_item_id": inventory_item_id,
        "location_id": location_id,
        "available_adjustment": adjustment
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()