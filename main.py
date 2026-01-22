from fastapi import FastAPI
from database import engine, Base
from routers import users
from fastapi.middleware.cors import CORSMiddleware


# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:5173",    # The URL of your Vite app
    "http://127.0.0.1:5173",    # Alternative localhost URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # Allow your frontend
    allow_credentials=True,
    allow_methods=["*"],        # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],        # Allow all headers
)

app.include_router(users.router, prefix="/users", tags=["Users"])

@app.get("/")
def read_root():
    return {"message": "Security Module is Active"}