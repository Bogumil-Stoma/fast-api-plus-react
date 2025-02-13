import os

DB_HOST: str = os.getenv("POSTGRES_HOST", "postgres")  # Docker service name
DB_PORT: str = os.getenv("POSTGRES_PORT", "5432")
DB_USER: str = os.getenv("POSTGRES_USER", "myuser")
DB_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "mypassword")
DB_NAME: str = os.getenv("POSTGRES_DB", "mydatabase")

def database_url() -> str:
    return f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
