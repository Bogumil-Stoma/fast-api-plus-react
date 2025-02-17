from typing import Union, Annotated

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from database.database import get_db
from models.user_model import User
from schemas.user_schema import UserCreate
from services.user_service import create_user
from utils.security import hash_password, verify_password, create_access_token, decode_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError

from schemas.token_schema import TokenData, Token

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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
    existing_user = await db.execute(text("SELECT * FROM users WHERE username = :username"), {"username": user.username})
    if existing_user.fetchone():
        raise HTTPException(status_code=400, detail="Username already registered")

    new_user = await create_user(db, user.username, user.password, user.email, user.phone_number, is_admin=False)
    return {"message": "User created successfully", "user_id": new_user.id}

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = await db.execute(text("SELECT * FROM users where username=:username"), {"username": token_data.username})
    user = user.fetchone()
    if user is None:
        raise credentials_exception
    return user

@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: AsyncSession = Depends(get_db)
) -> Token:
    result = await db.execute(text("SELECT * FROM users WHERE username = :username"), {"username": form_data.username})
    user = result.fetchone()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.username}
    )
    return Token(access_token=access_token, token_type="bearer")

@app.get("/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    result = current_user.email
    return {"email": result}