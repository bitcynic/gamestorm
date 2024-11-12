from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from gamestorm.services.auth_service import AuthService
from gamestorm.repositories.user_repository import UserRepository
from gamestorm.utils.security import create_ln_invoice
from gamestorm.dependencies import get_db
from gamestorm.schemas.user import UserCreate, AuthResponse

auth_router = APIRouter()

@auth_router.post("/authenticate", response_model=AuthResponse)
def authenticate(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Authenticates a user and returns a Lightning Network invoice.
    """
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)
    user = auth_service.authenticate(user_in.username, user_in.ln_address)
    ln_invoice = create_ln_invoice(user.ln_address)
    return AuthResponse(ln_invoice=ln_invoice, user_id=user.id)

@auth_router.post("/authenticate/confirm")
def authenticate_confirm(signed_invoice: str):
    """
    Confirms the authentication by verifying the signed invoice.
    """
    # TODO: Implement verification of the signed invoice
    return {"status": "Authentication successful"}

