import requests
from gamestorm.config import settings

class ZebedeeClient:
    """Client for interacting with the ZEBEDEE API."""
    def __init__(self):
        self.api_key = settings.API_KEY
        self.base_url = "https://api.zebedee.io/v0"

    def fetch_charge(self, amount: int, ln_address: str, description: str):
        """
        Creates a Lightning Network charge to request payment.
        """
        url = f"{self.base_url}/ln-address/fetch-charge"
        headers = {
            "Content-Type": "application/json",
            "apikey": self.api_key
        }
        data = {
            "amount": amount,
            "lnAddress": ln_address,
            "description": description
        }
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()

    def check_charge_status(self, charge_id: str):
        """
        Checks the status of a charge.
        """
        url = f"{self.base_url}/charges/{charge_id}"
        headers = {
            "Content-Type": "application/json",
            "apikey": self.api_key
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

