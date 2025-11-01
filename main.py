import os
from fernet_utils import decrypt_env_value
from faucetpay_client import FaucetPayClient
from telegram_bot import start_bot

def check_env_vars():
    """Vérifie la présence des variables d'environnement essentielles"""
    required_vars = ["FERNET_KEY", "FAUCETPAY_API_KEY_ENCRYPTED", "TELEGRAM_BOT_TOKEN"]
    missing = [v for v in required_vars if not os.getenv(v)]
    if missing:
        raise EnvironmentError(f"❌ Variables manquantes : {', '.join(missing)}")
    print("✅ Toutes les variables d'environnement nécessaires sont présentes.")


def test_faucetpay_connection():
    """Teste la connexion à FaucetPay"""
    print("🔄 Test de connexion à FaucetPay...")
    try:
        fp = FaucetPayClient()
        balance = fp.get_balance("BTC")
        if balance.get("status") == 200:
            print(f"💰 Solde FaucetPay récupéré avec succès : {balance.get('balance', 'N/A')} BTC")
        else:
            print(f"⚠️ Réponse inattendue de FaucetPay : {balance}")
    except Exception as e:
        print(f"❌ Erreur lors du test FaucetPay : {e}")


def launch_bot():
    """Démarre le bot Telegram"""
    print("🤖 Lancement du bot Telegram Bitcoin09...")
    try:
        start_bot()
    except Exception as e:
        print(f"❌ Erreur au démarrage du bot : {e}")


if __name__ == "__main__":
    print("🚀 Initialisation du projet Bitcoin09_final...")
    check_env_vars()
    test_faucetpay_connection()
    launch_bot()
