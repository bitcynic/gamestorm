from gamestorm.database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends

def get_db():
    """Dependency that provides a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

