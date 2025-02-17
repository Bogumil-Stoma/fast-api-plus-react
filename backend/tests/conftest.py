import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from backend.models.user_model import Base


DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(DATABASE_URL, echo=True, future=True)
TestSessionLocal = async_sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False)

@pytest_asyncio.fixture()
async def test_db():
    """Fixture to set up and tear down the test database"""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create a session and provide it to the test
    async with TestSessionLocal() as session:
        yield session  # This session will be used in the test

    # Cleanup after the test (drop the tables)
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
