# pyright: reportMissingImports=false
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine # type: ignore
from sqlalchemy import text # type: ignore
import os
from dotenv import load_dotenv # type: ignore

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:1234@localhost:5432/fair_hiring")

async def clear_data():
    engine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        try:
            # Delete all candidates. Foreign key constraints with ON DELETE CASCADE
            # will automatically delete related applications, credentials, and review_cases.
            result = await conn.execute(text("DELETE FROM candidates;"))
            print(f"✅ Deleted {result.rowcount} candidates (and their related applications due to cascade).")
        except Exception as e:
            print(f"Error: {e}")
    await engine.dispose()

asyncio.run(clear_data())
