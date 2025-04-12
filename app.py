from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles  # Add this import

from main import router as chat_router
from date import router as date_router

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your API routers
app.include_router(chat_router, prefix="/chat")
app.include_router(date_router, prefix="/date")

# Serve static files (HTML, JS, CSS)
app.mount("/", StaticFiles(directory=".", html=True), name="static")
