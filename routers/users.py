from fastapi import APIRouter, Depends, HTTPException, status, Query, Cookie
from typing import List, Optional
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from database import get_db
from models.user import User, UserRegister, UserLogin, UserResponse
from utils import hash_password, verify_password, create_access_token, SECRET_KEY, ALGORITHM

router = APIRouter()

security = HTTPBearer(auto_error=False)

def get_current_user(
    token_auth: Optional[HTTPAuthorizationCredentials] = Depends(security), 
    query_token: Optional[str] = Query(None, alias="token"), 
    cookie_token: Optional[str] = Cookie(None, alias="access_token"),
    db: Session = Depends(get_db)
):
    token = None

    if token_auth:
        token = token_auth.credentials
    elif query_token:
        token = query_token
    elif cookie_token:
        token = cookie_token.replace("Bearer ", "")

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You must be logged in first.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if not token:
        raise credentials_exception

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

@router.post("/register", response_model=UserResponse)
def register_user(user_req: UserRegister, db: Session = Depends(get_db)):
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

@router.post("/login")
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == login_data.username).first()
    
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/", response_model=List[UserResponse]) 
def get_all_users(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    users = db.query(User).all()
    return users