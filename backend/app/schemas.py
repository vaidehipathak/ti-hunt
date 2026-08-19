from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SourceOut(BaseModel):
    id: int
    name: str
    trust_score: float
    is_throttled: bool

    class Config:
        from_attributes = True


class AlertIn(BaseModel):
    source_name: str
    ioc_type: str
    ioc_value: str
    mitre_ttp: Optional[str] = None


class AlertOut(BaseModel):
    id: int
    source_id: int
    ioc_type: str
    ioc_value: str
    forwarded_to_siem: bool
    verdict: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class FeedbackIn(BaseModel):
    alert_id: int
    verdict: str   # "true_positive" | "false_positive"