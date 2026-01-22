import os
import httpx
import secrets
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from utils import create_access_token, hash_password

router = APIRouter()

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
GITHUB_REDIRECT_URI = "http://localhost:8000/auth/github/callback"

@router.get("/github/login")
async def github_login():
    return RedirectResponse(
        f"https://github.com/login/oauth/authorize?client_id={GITHUB_CLIENT_ID}&redirect_uri={GITHUB_REDIRECT_URI}&scope=user:email"
    )

@router.get("/github/callback")
async def github_callback(code: str, db: Session = Depends(get_db)):
    async with httpx.AsyncClient() as client:
        token_res = await client.post(
            "https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            data={
                "client_id": GITHUB_CLIENT_ID,
                "client_secret": GITHUB_CLIENT_SECRET,
                "code": code,
                "redirect_uri": GITHUB_REDIRECT_URI,
            },
        )
        token_data = token_res.json()
        access_token = token_data.get("access_token")
        
        if not access_token:
            raise HTTPException(status_code=400, detail="Failed to get access token from GitHub")

        user_res = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        user_data = user_res.json()

        email_res = await client.get(
            "https://api.github.com/user/emails",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        emails = email_res.json()
        primary_email = next((e["email"] for e in emails if e["primary"] and e["verified"]), None)

        if not primary_email:
            raise HTTPException(status_code=400, detail="No verified email found")

    user = db.query(User).filter(User.email == primary_email).first()

    if not user:
        random_password = secrets.token_urlsafe(16)
        new_user = User(
            username=user_data["login"],
            fullname=user_data.get("name") or user_data["login"],
            email=primary_email,
            hashed_password=hash_password(random_password),
            github_id=user_data["id"],
            avatar_url=user_data.get("avatar_url"),
            auth_provider="github"
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        user = new_user
    else:
        user.github_id = user_data["id"]
        user.avatar_url = user_data.get("avatar_url")
        user.auth_provider = "github"
        db.commit()

    jwt_token = create_access_token(data={"sub": user.username})

    # Redirect to the Official Frontend on Port 5173
    # The frontend code there will grab '?token=...' and save it.
    return RedirectResponse(url=f"http://localhost:5173/?token={jwt_token}")