from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from gamestorm.config import settings

# Create the SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
