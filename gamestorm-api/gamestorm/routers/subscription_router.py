from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from gamestorm.repositories.user_repository import UserRepository
from gamestorm.services.payment_service import PaymentService
from gamestorm.services.zebedee_client import ZebedeeClient
from gamestorm.dependencies import get_db
from gamestorm.schemas.user import (
    SubscriptionStatusResponse,
    ChargeResponse,
    PaymentVerificationResponse,
)
from pydantic import BaseModel

subscription_router = APIRouter()

class SubscribeRequest(BaseModel):
    user_id: int
    amount: int = 1000

class VerifyPaymentRequest(BaseModel):
    charge_id: str
    user_id: int

@subscription_router.get("/subscriptionStatus", response_model=SubscriptionStatusResponse)
def subscription_status(user_id: int, db: Session = Depends(get_db)):
    """
    Returns the subscription status of a user.
    """
    user_repo = UserRepository(db)
    user = user_repo.get_by_id(user_id)
    if user and user.subscription_active:
        return SubscriptionStatusResponse(status="subscribed")
    else:
        return SubscriptionStatusResponse(status="unsubscribed")

@subscription_router.post("/subscribe", response_model=ChargeResponse)
def subscribe(request: SubscribeRequest, db: Session = Depends(get_db)):
    """
    Creates a subscription charge for the user.
    """
    user_repo = UserRepository(db)
    zebedee_client = ZebedeeClient()
    payment_service = PaymentService(zebedee_client, user_repo)
    try:
        charge = payment_service.create_subscription_charge(request.user_id, request.amount)
        return ChargeResponse(
            ln_invoice=charge['data']['invoiceRequest'],
            charge_id=charge['data']['id']
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@subscription_router.post("/verify-payment", response_model=PaymentVerificationResponse)
def verify_payment(request: VerifyPaymentRequest, db: Session = Depends(get_db)):
    """
    Verifies the payment and activates the subscription.
    """
    user_repo = UserRepository(db)
    zebedee_client = ZebedeeClient()
    payment_service = PaymentService(zebedee_client, user_repo)
    payment_verified = payment_service.verify_payment(request.charge_id, request.user_id)
    if payment_verified:
        return PaymentVerificationResponse(status="Subscription activated")
    else:
        return PaymentVerificationResponse(status="Payment not completed")

