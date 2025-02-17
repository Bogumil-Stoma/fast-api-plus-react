import os

DB_HOST: str = os.getenv("POSTGRES_HOST")  # Docker service name
DB_PORT: str = os.getenv("POSTGRES_PORT")
DB_USER: str = os.getenv("POSTGRES_USER")
DB_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
DB_NAME: str = os.getenv("POSTGRES_DB")

def database_url() -> str:
    return f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
