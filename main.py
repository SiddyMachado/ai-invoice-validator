from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.database import engine, Base
from app.api import documents

# -------------------------------
# APP INIT
# -------------------------------
app = FastAPI(title="AI Document Reader API")

# -------------------------------
# CORS
# -------------------------------
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# DATABASE INIT
# -------------------------------
Base.metadata.create_all(bind=engine)

# -------------------------------
# ROUTERS
# -------------------------------
app.include_router(documents.router)

# -------------------------------
# HEALTH CHECK (optional but useful)
# -------------------------------
@app.get("/health")
def health_check():
    return {"status": "ok"}