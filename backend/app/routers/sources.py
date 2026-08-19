from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Source
from app.schemas import SourceOut

router = APIRouter(prefix="/api/v1", tags=["sources"])

@router.get("/sources", response_model=list[SourceOut])
def list_sources(db: Session = Depends(get_db)):
    return db.query(Source).all()