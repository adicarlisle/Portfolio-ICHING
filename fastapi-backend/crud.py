from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import Query
from schemas import TaskCreate, TaskUpdate, QueryCreate
from typing import List, Optional
from datetime import datetime

def get_task(db: Session, task_id: int) -> Optional[Task]:
    """Retrieve a task by ID"""
    return db.query(Task).filter(Task.id == task_id).first()

def get_tasks(db: Session, skip: int = 0, limit: int = 100) -> List[Task]:
    """Retrieve all tasks with pagination"""
    return db.query(Task).offset(skip).limit(limit).all()

def create_task(db: Session, task: TaskCreate) -> Task:
    """Create a new task"""
    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task_update: TaskUpdate) -> Optional[Task]:
    """Update an existing task"""
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        return None
    
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int) -> bool:
    """Delete a task"""
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        return False
    
    db.delete(db_task)
    db.commit()
    return True

def create_query(db: Session, query: QueryCreate, query_vector: list, hexagram_set: list):
    db_query = Query(
        query=query.query,
        query_vector=query_vector,
        hexagram_set=hexagram_set
    )
    db.add(db_query)
    db.commit()
    db.refresh(db_query)
    return db_query

def get_query(db: Session, query_id: int):
    return db.query(Query).filter(Query.id == query_id).first()

def get_queries(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Query).offset(skip).limit(limit).all()