from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession,async_sessionmaker
from database.config import database_url


engine = create_async_engine(database_url(), echo=True, future=True)

# Create async session
async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db():
    async with async_session() as session:
        yield session
