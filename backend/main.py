from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pathlib import Path
from starlette.middleware.sessions import SessionMiddleware
import os

from .database import engine, Base
from . import models
from .routers import products, warehouses, operations, auth

env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# Create tables
models.Base.metadata.create_all(bind=engine)

# Seed database with sample data
from .seed_data import seed_database
seed_database()

app = FastAPI(title="StockMaster API", description="Inventory Management System Backend")

# Production CORS Configuration
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

# Allow both production and development URLs
origins = [
    FRONTEND_URL,
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:3000",
]

# In production, you can also allow all origins (or be more specific)
if os.getenv("ENVIRONMENT") == "production":
    origins = ["*"]  # Or specify your Vercel domain

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if os.getenv("ENVIRONMENT") != "production" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to StockMaster API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Add Session Middleware for Authlib
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY", "secret"))

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(warehouses.router)
app.include_router(operations.router)
