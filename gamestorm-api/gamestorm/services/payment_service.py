from gamestorm.services.zebedee_client import ZebedeeClient
from gamestorm.repositories.user_repository import UserRepository
from datetime import datetime, timedelta

class PaymentService:
    """Service for handling payments and subscriptions."""
    def __init__(self, zebedee_client: ZebedeeClient, user_repo: UserRepository):
        self.zebedee_client = zebedee_client
        self.user_repo = user_repo

    def create_subscription_charge(self, user_id: int, amount: int):
        """
        Creates a charge for a user to subscribe.
        """
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        charge = self.zebedee_client.fetch_charge(
            amount=amount,
            ln_address=user.ln_address,
            description="Subscription Payment"
        )
        return charge

    def verify_payment(self, charge_id: str, user_id: int):
        """
        Verifies if the payment has been completed and updates the user's subscription status.
        """
        status = self.zebedee_client.check_charge_status(charge_id)
        if status['data']['status'] == 'completed':
            user = self.user_repo.get_by_id(user_id)
            user.subscription_active = True
            user.subscription_expires_at = datetime.now() + timedelta(days=30)
            self.user_repo.update(user)
            return True
        return False

