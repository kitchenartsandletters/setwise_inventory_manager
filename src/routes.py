from fastapi import APIRouter, Request
from .utils import verify_shopify_webhook
from .shopify import (
    get_product_by_handle,
    get_inventory_item_id,
    get_location_id,
    adjust_inventory
)
import json
from pathlib import Path

with open(Path(__file__).parent.parent / "bundle_map.json") as f:
    bundle_map = json.load(f)

router = APIRouter()

@router.post("/webhook")
async def receive_webhook(request: Request):
    await verify_shopify_webhook(request)
    payload = await request.json()

    order_id = payload.get("id")
    line_items = payload.get("line_items", [])

    print(f"🧾 Order {order_id} contains {len(line_items)} line item(s)")

    location_id = await get_location_id()

    for item in line_items:
        handle = item.get("title", "").lower().replace(" ", "-")
        quantity = item.get("quantity", 0)

        if handle in bundle_map:
            print(f"📦 Set detected: {handle} (qty: {quantity})")
            for component_handle in bundle_map[handle]:
                product = await get_product_by_handle(component_handle)
                inventory_item_id = await get_inventory_item_id(product)

                if inventory_item_id and location_id:
                    print(f"➖ Adjusting inventory for '{component_handle}' by -{quantity}")
                    print("🔧 ADJUST PAYLOAD:")
                    print(f"  inventory_item_id: {inventory_item_id}")
                    print(f"  location_id: {location_id}")
                    print(f"  adjustment: {-quantity}")
                    await adjust_inventory(inventory_item_id, location_id, -quantity)
                else:
                    print(f"⚠️ Could not adjust inventory for '{component_handle}'")
        else:
            print(f"✅ '{handle}' is not a set. No action taken.")

    return {"status": "ok"}

@router.post("/webhook/cancelled")
async def receive_cancelled_webhook(request: Request):
    await verify_shopify_webhook(request)
    payload = await request.json()

    order_id = payload.get("id")
    line_items = payload.get("line_items", [])

    print(f"🔄 Cancelled order {order_id} contains {len(line_items)} line item(s)")

    location_id = await get_location_id()

    for item in line_items:
        handle = item.get("title", "").lower().replace(" ", "-")
        quantity = item.get("quantity", 0)

        if handle in bundle_map:
            print(f"📦 Set detected in cancelled order: {handle} (qty: {quantity})")
            for component_handle in bundle_map[handle]:
                product = await get_product_by_handle(component_handle)
                inventory_item_id = await get_inventory_item_id(product)

                if inventory_item_id and location_id:
                    print(f"➕ Reversing inventory for '{component_handle}' by +{quantity}")
                    print("🔧 ADJUST PAYLOAD:")
                    print(f"  inventory_item_id: {inventory_item_id}")
                    print(f"  location_id: {location_id}")
                    print(f"  adjustment: {quantity}")
                    await adjust_inventory(inventory_item_id, location_id, quantity)
                else:
                    print(f"⚠️ Could not reverse inventory for '{component_handle}'")
        else:
            print(f"✅ '{handle}' is not a set in cancelled order. No action taken.")

    return {"status": "ok"}

@router.post("/webhook/refund")
async def receive_refund_webhook(request: Request):
    await verify_shopify_webhook(request)
    payload = await request.json()

    refund_line_items = payload.get("refund_line_items", [])
    print(f"🔄 Refund received with {len(refund_line_items)} refund line item(s)")

    location_id = await get_location_id()

    for item in refund_line_items:
        if item.get("restock_type") == "cancel":
            print("↪️ Skipping refund line with restock_type 'cancel' to avoid double adjustment")
            continue
        line_item = item.get("line_item", {})
        handle = line_item.get("title", "").lower().replace(" ", "-")
        quantity = item.get("quantity", 0)

        if handle in bundle_map:
            print(f"📦 Set detected in refund: {handle} (qty: {quantity})")
            for component_handle in bundle_map[handle]:
                product = await get_product_by_handle(component_handle)
                inventory_item_id = await get_inventory_item_id(product)

                if inventory_item_id and location_id:
                    print(f"➕ Reversing inventory for '{component_handle}' by +{quantity}")
                    print("🔧 ADJUST PAYLOAD:")
                    print(f"  inventory_item_id: {inventory_item_id}")
                    print(f"  location_id: {location_id}")
                    print(f"  adjustment (reversal): +{quantity}")
                    await adjust_inventory(inventory_item_id, location_id, quantity)
                else:
                    print(f"⚠️ Could not reverse inventory for '{component_handle}'")
        else:
            print(f"✅ '{handle}' is not a set in refund. No action taken.")

    return {"status": "ok"}

@router.get("/health")
def health_check():
    return {"status": "ok"}