from sqlalchemy.ext.asyncio import AsyncSession
from models.user_model import User
from utils.security import hash_password

async def create_user(db: AsyncSession, username: str, password: str, email: str, phone_number: str, is_admin: bool = False):
    hashed_password = hash_password(password)
    new_user = User(username=username, password_hash=hashed_password, email=email, phone_number=phone_number, is_admin=is_admin)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def create_admin(db: AsyncSession, username: str, password: str, email: str, phone_number: str):
    new_user = await create_user(db, username, password, email, phone_number, is_admin=True)
    return new_user