from sqlalchemy.orm import Session
from typing import Optional
from gamestorm.models.user import User as UserModel

class UserRepository:
    """Repository for interacting with User data in the database."""
    def __init__(self, db: Session):
        self.db = db

    def save(self, user: UserModel):
        """Saves a user to the database."""
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

    def get_by_id(self, user_id: int) -> Optional[UserModel]:
        """Retrieves a user by their ID."""
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()

    def get_by_username(self, username: str) -> Optional[UserModel]:
        """Retrieves a user by their username."""
        return self.db.query(UserModel).filter(UserModel.username == username).first()

    def update(self, user: UserModel):
        """Updates an existing user in the database."""
        self.db.merge(user)
        self.db.commit()
        self.db.refresh(user)

