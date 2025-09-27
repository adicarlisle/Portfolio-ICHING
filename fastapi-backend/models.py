from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from database import Base
from datetime import datetime

class Query(Base):
    __tablename__ = "queries"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(Text, nullable=False)
    query_vector = Column(JSON, nullable=False)  # Store vector as JSON array
    hexagram_set = Column(JSON, nullable=False)  # Store hexagram indices and scores
    created_at = Column(DateTime, server_default=func.now(), nullable=False)