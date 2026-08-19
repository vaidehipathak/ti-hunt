from sqlalchemy.orm import Session
from app.models import Source
from app.bandit.exp3 import EXP3
from app.watchdog.cusum import CUSUMWatchdog
from app.config import settings

bandit = EXP3(gamma=0.1)
watchdog = CUSUMWatchdog(k=0.05, h=0.3)


def get_or_create_source(db: Session, name: str) -> Source:
    source = db.query(Source).filter(Source.name == name).first()
    if not source:
        source = Source(name=name, weight=1.0, trust_score=0.5)
        db.add(source)
        db.commit()
        db.refresh(source)
    return source


def recompute_trust_score(db: Session, source: Source):
    all_sources = db.query(Source).all()
    total_weight = sum(s.weight for s in all_sources)
    prob = bandit.get_probability(source.weight, total_weight, len(all_sources))
    source.trust_score = prob
    source.is_throttled = prob < settings.siem_trust_threshold
    db.commit()


def apply_feedback(db: Session, source: Source, reward: float):
    all_sources = db.query(Source).all()
    total_weight = sum(s.weight for s in all_sources)
    prob = bandit.get_probability(source.weight, total_weight, len(all_sources))

    source.weight = bandit.update_weight(
        source.weight, prob, reward, len(all_sources)
    )
    db.commit()
    recompute_trust_score(db, source)

    # feed the new trust score into the watchdog for anomaly detection
    is_anomalous = watchdog.update(source.name, source.trust_score)
    if is_anomalous:
        source.is_throttled = True
        db.commit()