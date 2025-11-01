"""Module pour gérer les fonctions Scan, Compte et Transfère du bot."""
import time
import random
from faucetpay_client import FaucetPayClient

def scan():
    """Simule un scan Bitcoin et retourne le montant trouvé."""
    time.sleep(1)
    amt = round(random.uniform(0.00001, 0.0005), 8)
    return {"ok": True, "found": [amt], "total": amt}

def get_account():
    """Retourne le solde du compte FaucetPay."""
    client = FaucetPayClient()
    try:
        data = client.get_balance("BTC")
        if data.get("status") == 200:
            bal = float(data.get("balance", {}).get("BTC", {}).get("balance", 0))
        else:
            bal = 0.0
        return {"ok": True, "balance": bal, "currency": "BTC"}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def transfer(amount, destination, method="faucetpay"):
    """Transfère un montant à l'adresse/email spécifié via FaucetPay."""
    client = FaucetPayClient()
    try:
        resp = client.send(to=destination, amount=amount, currency="BTC")
        return {"ok": True, "result": resp}
    except Exception as e:
        return {"ok": False, "error": str(e)}
