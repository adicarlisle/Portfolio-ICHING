from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import List, Optional

class QueryBase(BaseModel):
    query: str

class QueryCreate(QueryBase):
    pass

class HexagramScore(BaseModel):
    hexagram_id: int
    hexagram_name: str
    hexagram_unicode: str
    score: float

class QueryResponse(QueryBase):
    id: int
    query_vector: List[float]
    hexagram_set: List[HexagramScore]
    created_at: datetime

    class Config:
        orm_mode = True