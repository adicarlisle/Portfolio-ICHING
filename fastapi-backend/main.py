from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import Base, engine, get_db
from services.iching_embeddings import ICHingEmbeddingService
import numpy as np

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI instance
app = FastAPI(
    title="I Ching Query API",
    description="API for I Ching query processing with hexagram analysis",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://react-frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize embedding service
embedding_service = ICHingEmbeddingService()

@app.get("/", tags=["Health"])
def read_root():
    """Health check endpoint"""
    return {"status": "healthy", "service": "I Ching Query API"}

@app.post("/queries/", response_model=schemas.QueryResponse, tags=["Queries"])
def create_query(query: schemas.QueryCreate, db: Session = Depends(get_db)):
    # Generate vector embedding and hexagram set for the query
    query_vector, hexagram_set = embedding_service.process_query(query.query)
    
    # Create database record
    db_query = models.Query(
        query=query.query,
        query_vector=query_vector,
        hexagram_set=hexagram_set
    )
    db.add(db_query)
    db.commit()
    db.refresh(db_query)
    
    return db_query

@app.get("/queries/", response_model=List[schemas.QueryResponse], tags=["Queries"])
def read_queries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    queries = db.query(models.Query).offset(skip).limit(limit).all()
    return queries

@app.get("/queries/{query_id}", response_model=schemas.QueryResponse, tags=["Queries"])
def read_query(query_id: int, db: Session = Depends(get_db)):
    query = db.query(models.Query).filter(models.Query.id == query_id).first()
    if query is None:
        raise HTTPException(status_code=404, detail="Query not found")
    return query

@app.get("/queries/search/similar", tags=["Queries"])
def find_similar_queries(query: str, limit: int = 10, db: Session = Depends(get_db)):
    """Find queries with similar vector embeddings"""
    # Generate vector for search query
    search_vector, _ = embedding_service.process_query(query)
    search_vector = np.array(search_vector)
    
    # Get all queries from database
    all_queries = db.query(models.Query).all()
    
    # Calculate cosine similarity
    similarities = []
    for db_query in all_queries:
        db_vector = np.array(db_query.query_vector)
        
        # Cosine similarity
        similarity = np.dot(search_vector, db_vector) / (np.linalg.norm(search_vector) * np.linalg.norm(db_vector))
        similarities.append((db_query, similarity))
    
    # Sort by similarity and return top results
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    return [
        {
            "id": query.id,
            "query": query.query,
            "similarity": float(similarity),
            "hexagram_set": query.hexagram_set,
            "created_at": query.created_at
        }
        for query, similarity in similarities[:limit]
    ]

@app.get("/hexagrams/", tags=["Hexagrams"])
def get_hexagrams():
    """Get all available hexagrams"""
    return [
        {
            "id": hex_data[0],
            "name": hex_data[1],
            "keyword": hex_data[2],
            "unicode": hex_data[3]
        }
        for hex_data in embedding_service.hexagrams
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)