from gamestorm.models.user import User as UserModel
from gamestorm.repositories.user_repository import UserRepository

class AuthService:
    """Service for handling user authentication."""
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def authenticate(self, username: str, ln_address: str) -> UserModel:
        """
        Authenticates a user, creating a new user if necessary.
        """
        # Check if the user already exists
        existing_user = self.user_repo.get_by_username(username)
        if existing_user:
            return existing_user

        # Create a new user
        user = UserModel(
            username=username,
            ln_address=ln_address
        )
        self.user_repo.save(user)
        return user

