from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware        # ← import
from api.LeadRoute import router as Lead_router

app = FastAPI()

# create any required schema before the first request
from db.database import init_db

@app.on_event("startup")
def startup_event():
    init_db()


# allow the front‑end origin(s) to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # React default
        "http://localhost:5173",      # Vite dev server
        "http://127.0.0.1:5173",      # sometimes used by fetch
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(Lead_router)