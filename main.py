from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import app as api_app

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the entire API under /api  (frontend calls /api/...)
app.mount("/api", api_app)
