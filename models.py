from sqlalchemy import Column, Integer, Text, DateTime
from datetime import datetime
from database import Base


class ApiData(Base):
    __tablename__ = "api_data"

    id = Column(Integer, primary_key=True, index=True)

    source_name = Column(Text, nullable=False)

    api_url = Column(Text, nullable=False)

    status_code = Column(Integer, nullable=False)

    response = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)


class IngestionRun(Base):
    __tablename__ = "ingestion_runs"

    id = Column(Integer, primary_key=True, index=True)

    status = Column(Text, nullable=False)

    total_sources = Column(Integer, nullable=False)

    successful_sources = Column(Integer, nullable=False, default=0)

    failed_sources = Column(Integer, nullable=False, default=0)

    started_at = Column(DateTime, default=datetime.utcnow)

    completed_at = Column(DateTime, nullable=True)