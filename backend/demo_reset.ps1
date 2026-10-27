# Run from backend/ with uvicorn already running and venv active
python -c "from app.database import Base, engine; import app.models; Base.metadata.drop_all(bind=engine); Base.metadata.create_all(bind=engine); print('reset ok')"
python -m ingestion.urlhaus_pull
python -m ingestion.threatfox_pull
python -m simulation.harness --rounds 30