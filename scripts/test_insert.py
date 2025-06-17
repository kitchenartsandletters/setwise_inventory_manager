import asyncio
from src.db import db

async def test_insert():
    async with db.engine.begin() as conn:
        await conn.execute(
            db.processed_events.insert().values(
                order_id="TEST123",
                event_type="test_event"
            )
        )
    print("✅ Test insert completed")

if __name__ == "__main__":
    asyncio.run(test_insert())
