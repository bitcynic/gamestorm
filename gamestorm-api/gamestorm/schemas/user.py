from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str
    ln_address: str

    @validator('ln_address')
    def validate_ln_address(cls, v):
        if '@' not in v:
            raise ValueError('Invalid Lightning Network address')
        return v

class UserCreate(UserBase):
    pass

class UserResponse(BaseModel):
    id: int
    username: str
    ln_address: str
    subscription_active: bool
    subscription_expires_at: Optional[datetime]

    class Config:
        orm_mode = True

class AuthResponse(BaseModel):
    ln_invoice: str
    user_id: int

class SubscriptionStatusResponse(BaseModel):
    status: str

class ChargeResponse(BaseModel):
    ln_invoice: str
    charge_id: str

class PaymentVerificationResponse(BaseModel):
    status: str

