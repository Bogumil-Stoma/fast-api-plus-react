import pytest

import os
print(os.getcwd())
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.user_model import User
from services.user_service import create_user, create_admin  # Adjust the import path

@pytest.mark.asyncio
async def test_create_user(test_db: AsyncSession):
    """Test creating a regular user"""

    user = await create_user(
        test_db,
        username="testuser",
        password="securepassword",
        email="test@example.com",
        phone_number="1234567890",
        is_admin=False
    )

    assert user.id is not None
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.is_admin is False

    result = await test_db.execute(select(User).where(User.email == "test@example.com"))
    print(result)
    db_user = result.scalars().first()
    assert db_user is not None
    assert db_user.username == "testuser"

@pytest.mark.asyncio
async def test_create_admin(test_db: AsyncSession):
    """Test creating an admin user"""
    admin = await create_admin(
        test_db,
        username="adminuser",
        password="securepassword",
        email="admin@example.com",
        phone_number="9876543210"
    )

    assert admin.id is not None
    assert admin.username == "adminuser"
    assert admin.email == "admin@example.com"
    assert admin.is_admin is True

    result = await test_db.execute(select(User).where(User.email == "admin@example.com"))
    db_admin = result.scalars().first()
    assert db_admin is not None
    assert db_admin.username == "adminuser"
