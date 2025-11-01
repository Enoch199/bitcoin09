"""Module utilitaire pour chiffrer et déchiffrer des valeurs avec Fernet."""
import os
from cryptography.fernet import Fernet

def encrypt_value(plain: str, key: str) -> str:
    """Chiffre une chaîne en utilisant la clé Fernet fournie."""
    f = Fernet(key.encode())
    return f.encrypt(plain.encode()).decode()

def decrypt_env_value(value: str) -> str:
    """Déchiffre une valeur à partir de la variable d'environnement FERNET_KEY."""
    key = os.getenv("FERNET_KEY")
    if not key:
        raise ValueError("FERNET_KEY not set in environment")
    f = Fernet(key.encode())
    return f.decrypt(value.encode()).decode()
