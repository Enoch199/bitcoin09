#!/usr/bin/env python3
"""
encrypt_key.py
Génère une FERNET_KEY (ou utilise celle fournie) et chiffre une FaucetPay API key.
Usage:
  python encrypt_key.py              # te demande la clé API puis génère une FERNET_KEY
  python encrypt_key.py --key ABC... # utilise la FERNET_KEY fournie
Options:
  --save-env     : crée/ajoute à .env (dans le répertoire courant) les variables FERNET_KEY et FAUCETPAY_API_KEY_ENCRYPTED
"""

import argparse
import getpass
from cryptography.fernet import Fernet
import os
import sys

def generate_key() -> str:
    return Fernet.generate_key().decode()

def encrypt(api_key: str, key: str) -> str:
    f = Fernet(key.encode())
    return f.encrypt(api_key.encode()).decode()

def main():
    parser = argparse.ArgumentParser(description="Génère FERNET_KEY et chiffre une FaucetPay API key.")
    parser.add_argument("--key", "-k", help="FERNET_KEY existante (optionnel). Si omise, une nouvelle clé est générée.")
    parser.add_argument("--save-env", action="store_true", help="Sauvegarder la FERNET_KEY et FAUCETPAY_API_KEY_ENCRYPTED dans .env (ajoute/écrase).")
    args = parser.parse_args()

    fernet_key = args.key or generate_key()
    if not args.key:
        print(f"[+] Nouvelle FERNET_KEY générée: {fernet_key}")

    # Saisir la FaucetPay API key sans l'afficher
    try:
        api_key = getpass.getpass("Entrer votre FaucetPay API key (ne s'affichera pas) : ")
    except Exception as e:
        print("Erreur lors de la saisie :", e)
        sys.exit(1)

    if not api_key:
        print("Aucune clé fournie, sortie.")
        sys.exit(1)

    # Chiffrement
    encrypted = encrypt(api_key, fernet_key)
    print("\n[+] Valeur chiffrée (FAUCETPAY_API_KEY_ENCRYPTED) :")
    print(encrypted)

    if args.save_env:
        env_path = ".env"
        # Lecture existante
        env = {}
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    if "=" in line:
                        k, v = line.strip().split("=", 1)
                        env[k] = v

        # Mettre à jour
        env["FERNET_KEY"] = fernet_key
        env["FAUCETPAY_API_KEY_ENCRYPTED"] = encrypted

        # Écrire
        with open(env_path, "w", encoding="utf-8") as f:
            for k, v in env.items():
                f.write(f"{k}={v}\n")
        print(f"[+] Variables écrites dans {env_path} (FERNET_KEY & FAUCETPAY_API_KEY_ENCRYPTED)")

    else:
        print("\nInstructions :")
        print(" - Copie la FERNET_KEY suivante dans Render/GitHub secrets -> FERNET_KEY :")
        print(f"   {fernet_key}")
        print(" - Copie la valeur chiffrée dans FAUCETPAY_API_KEY_ENCRYPTED (Render / GitHub secrets).")
        print(" - Ne commite jamais ces valeurs dans un repo public.")

if __name__ == "__main__":
    main()
