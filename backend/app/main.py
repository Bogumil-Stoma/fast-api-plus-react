from typing import Union

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from database import get_db
from models import User
from schema import UserCreate
from crud import create_user

app = FastAPI()


@app.on_event("startup")
def on_startup():
    get_db()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/users")
async def read_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text('SELECT * FROM users;'))
    users = result.mappings().all()
    return users

@app.post("/register/")
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await db.execute(text("SELECT * FROM users WHERE email = :email"), {"email": user.email})
    if existing_user.fetchone():
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = await create_user(db, user.username, user.password, user.email, user.phone_number, is_admin=False)
    return {"message": "User created successfully", "user_id": new_user.id}