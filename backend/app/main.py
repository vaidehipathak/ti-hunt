from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.config import settings
from app.routers import sources, alerts, feedback

Base.metadata.create_all(bind=engine)

app = FastAPI(title="TI-Hunt API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.cors_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sources.router)
app.include_router(alerts.router)
app.include_router(feedback.router)


@app.get("/health")
def health():
    return {"status": "ok"}