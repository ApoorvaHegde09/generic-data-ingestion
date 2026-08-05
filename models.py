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