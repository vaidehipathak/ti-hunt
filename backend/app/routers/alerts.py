from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Alert, Source
from app.schemas import AlertIn, AlertOut
from app.services.source_manager import get_or_create_source
from app.config import settings

router = APIRouter(prefix="/api/v1", tags=["alerts"])

@router.get("/alerts", response_model=list[AlertOut])
def list_alerts(db: Session = Depends(get_db)):
    return db.query(Alert).order_by(Alert.created_at.desc()).limit(100).all()


@router.post("/alerts", response_model=AlertOut)
def inject_alert(payload: AlertIn, db: Session = Depends(get_db)):
    source = get_or_create_source(db, payload.source_name)

    forwarded = source.trust_score >= settings.siem_trust_threshold

    alert = Alert(
        source_id=source.id,
        ioc_type=payload.ioc_type,
        ioc_value=payload.ioc_value,
        mitre_ttp=payload.mitre_ttp,
        forwarded_to_siem=forwarded,
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert