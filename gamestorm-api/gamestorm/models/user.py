from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from gamestorm.models.base import Base

class User(Base):
    """Represents a user in the database."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    ln_address = Column(String)
    subscription_active = Column(Boolean, default=False)
    subscription_expires_at = Column(DateTime, nullable=True)

