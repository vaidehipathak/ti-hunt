from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    weight = Column(Float, default=1.0)          # raw EXP3 weight
    trust_score = Column(Float, default=0.5)      # normalized probability (0-1)
    is_throttled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    alerts = relationship("Alert", back_populates="source")


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("sources.id"))
    ioc_type = Column(String)
    ioc_value = Column(String)
    mitre_ttp = Column(String, nullable=True)
    forwarded_to_siem = Column(Boolean, default=False)
    verdict = Column(String, nullable=True)   # "true_positive" | "false_positive" | None
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    source = relationship("Source", back_populates="alerts")


class SourceMetricWindow(Base):
    """Rolling window data used by the CUSUM watchdog per source."""
    __tablename__ = "source_metric_windows"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("sources.id"))
    volume = Column(Integer)
    trust_score_at_time = Column(Float)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))