import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# 1. Load environment variables
load_dotenv()

# 2. Get DB configuration
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "fastapi_week6")
# Default to 5432 if not set, but we set it to 5433 in .env previously
DB_PORT = os.getenv("DB_PORT", "5432") 

# 3. Create the Database URL
# IMPORTANT: Notice the colon before {DB_PORT}
SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 4. Define the engine (This is what was missing/not found!)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 5. Create SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 6. Create Base
Base = declarative_base()

# 7. Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()