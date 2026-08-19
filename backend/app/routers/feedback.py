from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Alert
from app.schemas import FeedbackIn
from app.services.source_manager import apply_feedback

router = APIRouter(prefix="/api/v1", tags=["feedback"])

@router.post("/feedback")
def submit_feedback(payload: FeedbackIn, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == payload.alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    alert.verdict = payload.verdict
    db.commit()

    reward = 1.0 if payload.verdict == "true_positive" else 0.0
    apply_feedback(db, alert.source, reward)

    return {"status": "ok", "source_trust_score": alert.source.trust_score}