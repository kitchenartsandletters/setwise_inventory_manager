import asyncio
from src.db import db

async def initialize():
    await db.init_schema()

if __name__ == "__main__":
    asyncio.run(initialize())