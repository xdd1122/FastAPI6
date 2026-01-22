from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from database import get_db
from models.user import User, UserRegister, UserLogin, UserResponse
from utils import hash_password, verify_password, create_access_token, SECRET_KEY, ALGORITHM

router = APIRouter()

# Defines where FastAPI looks for the token (header: Authorization: Bearer <token>)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

# --- Dependency: Verify Token ---
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

# --- Endpoint 1: Register ---
@router.post("/register", response_model=UserResponse)
def register_user(user_req: UserRegister, db: Session = Depends(get_db)):
    # Check if user exists
    if db.query(User).filter(User.username == user_req.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    
    new_user = User(
        username=user_req.username,
        fullname=user_req.fullname,
        email=user_req.email,
        hashed_password=hash_password(user_req.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# --- Endpoint 2: Login ---
@router.post("/login")
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    # logic changes: form_data.username -> login_data.username
    
    # 1. Query the user using the JSON data
    user = db.query(User).filter(User.username == login_data.username).first()
    
    # 2. Verify password using login_data
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    # 3. Create JWT Token (No changes here)
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# --- Endpoint 3: Protected Query ---
@router.get("/", response_model=list[UserResponse]) 
def get_all_users(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Get all users.
    URL: GET /users/
    """
    print(f"Request made by authorized user: {current_user.username}")
    users = db.query(User).all()
    return users