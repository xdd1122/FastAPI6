from sqlalchemy import Column, Integer, String
from pydantic import BaseModel, EmailStr
from database import Base

# --- SQLAlchemy Table ---
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    fullname = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

# --- Pydantic Schemas ---
class UserRegister(BaseModel):
    username: str
    fullname: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    username: str
    email: str
    fullname: str

    class Config:
        from_attributes = True # Allows Pydantic to read SQLAlchemy objects