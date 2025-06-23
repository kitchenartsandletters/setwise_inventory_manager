import os
import uuid
import json
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, text
from sqlalchemy.future import select

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


class ProcessedEvent(Base):
    __tablename__ = "processed_events"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, nullable=False)
    event_type = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=text("NOW()"))

class WebhookLog(Base):
    __tablename__ = "webhook_logs"

    id = Column(String, primary_key=True)
    order_id = Column(String, nullable=True)
    event_type = Column(String, nullable=False)
    payload_json = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=text("NOW()"))

class Database:
    def __init__(self):
        self.engine = engine
        self.async_session = AsyncSessionLocal

    async def init_schema(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print("✅ Schema initialized")

    async def has_been_processed(self, order_id: str, event_type: str) -> bool:
        async with self.async_session() as session:
            result = await session.execute(
                select(ProcessedEvent).where(
                    ProcessedEvent.order_id == str(order_id),
                    ProcessedEvent.event_type == event_type
                )
            )
            return result.scalar_one_or_none() is not None

    async def mark_as_processed(self, order_id: str, event_type: str):
        async with self.async_session() as session:
            event = ProcessedEvent(
                order_id=order_id,
                event_type=event_type,
                created_at=datetime.utcnow()
            )
            session.add(event)
            await session.commit()

    async def record_event(self, order_id: str, event_type: str):
        async with self.async_session() as session:
            event = ProcessedEvent(
                order_id=str(order_id),
                event_type=event_type,
                created_at=datetime.utcnow()
            )
            session.add(event)
            await session.commit()

    async def log_webhook(self, order_id: str, event_type: str, payload: dict):
        async with self.async_session() as session:
            uuid_val = str(uuid.uuid4())
            payload_json_str = json.dumps(payload)
            created_at = datetime.utcnow()
            await session.execute(
                text(
                    """
                    INSERT INTO webhook_logs (id, order_id, event_type, payload_json, created_at)
                    VALUES (:id, :order_id, :event_type, :payload_json, :created_at)
                    """
                ),
                {
                    "id": uuid_val,
                    "order_id": order_id,
                    "event_type": event_type,
                    "payload_json": payload_json_str,
                    "created_at": created_at,
                },
            )
            await session.commit()

    def get_table(self, name: str):
        return Base.metadata.tables.get(name)

db = Database()
db.processed_events = ProcessedEvent.__table__
db.webhook_logs = WebhookLog.__table__