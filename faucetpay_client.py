"""Module pour communiquer avec FaucetPay et gérer les opérations BTC."""
import os
import requests
from fernet_utils import decrypt_env_value

class FaucetPayClient:
    """Client pour interagir avec l’API FaucetPay."""
    def __init__(self):
        enc = os.getenv("FAUCETPAY_API_KEY_ENCRYPTED")
        if not enc:
            raise ValueError("FAUCETPAY_API_KEY_ENCRYPTED not set in env")
        self.api_key = decrypt_env_value(enc)
        self.base_url = "https://faucetpay.io/api/v1/"

    def get_balance(self, currency="BTC"):
        """Retourne le solde du compte pour la crypto spécifiée."""
        try:
            resp = requests.post(
                f"{self.base_url}balance",
                data={"api_key": self.api_key, "currency": currency},
                timeout=30
            )
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            return {"ok": False, "error": str(e)}

    def send(self, to, amount, currency="BTC"):
        """Envoie un montant à l’adresse/email spécifiée."""
        try:
            resp = requests.post(
                f"{self.base_url}send",
                data={"api_key": self.api_key, "to": to, "amount": amount, "currency": currency},
                timeout=30
            )
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            return {"ok": False, "error": str(e)}
