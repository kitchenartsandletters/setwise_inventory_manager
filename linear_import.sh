#!/bin/bash

lin new "📦 Phase 1: Webhook Listener & Project Scaffold" --description "Set up FastAPI app scaffold. Add local development via ngrok tunnel. Configure environment variables. Test Shopify webhook connectivity with a paid test order."

lin new "🔧 Phase 2: Inventory Adjustment Logic" --description "Parse bundle map and match line items. Adjust inventory via Shopify Admin API. Use `product_handle` or `barcode`, not SKU."

lin new "🧪 Phase 3: Refund and Cancellation Handling" --description "Register `/webhook/cancelled` and `/webhook/refund` endpoints. Ensure correct inventory adjustment for each. Avoid double-counting during cancellation + refund events."

lin new "📊 Phase 4: Debug Logging and Edge Case Patching" --description "Add debug logging to trace webhook flow and payload parsing. Patch edge cases including fallback to primary inventory location ID and bundle data loading issues."

lin new "🚀 Phase 5: Deployment to Railway" --description "Create and link Railway project. Set environment variables. Add start command or Nixpacks config. Validate inventory adjustment on live test orders."

lin new "🧱 Phase 6: Lightweight Idempotency Check" --description "Prevent duplicate webhook events from causing double inventory adjustments. Set up hashed signature or cache-based deduplication with expiration logic."

lin new "🗄️ Phase 7: Persistence with PostgreSQL (Railway DB)" --description "Provision PostgreSQL database in Railway. Add ORM model for `processed_events`. Scaffold database schema and initialize with Alembic or SQLAlchemy core."

lin new "🧪 Phase 8: Idempotency Enforcement via DB" --description "Use database to track webhook delivery IDs or hash. Check before adjusting inventory. Store processing time and bundle metadata."

lin new "📣 Phase 9: Slack Alert Integration" --description "Send Slack alert via SLACK_WEBHOOK_URL whenever inventory is adjusted due to bundles. Include order number, bundle title(s), and adjustment details."

lin new "📈 Phase 10: Logging Upgrade & Future Analytics" --description "Centralize logs through Railway’s Logs tab or plan future offboarding to persistent log/metrics store (e.g., Supabase or Logtail)."

lin new "🧪 Phase 11: Comprehensive System Tests" --description "Simulate various scenarios: single book order, bundle order, partial refunds, full refunds, cancellation-only, and webhook retries. Validate inventory behavior."

lin new "📦 Phase 12: Bundle Map Management" --description "Refactor `bundle_map.json` into a managed admin system or hosted data store. Support dynamic bundle rules in future iterations."