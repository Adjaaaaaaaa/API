""" pour exécuter le fichier:
python extract_users.py --max-users 300 --since 15000000  """

from dotenv import load_dotenv
import os
import requests
import json
import time
import argparse
from pathlib import Path
from datetime import datetime

# Charger les variables d'environnement
load_dotenv()
token = os.getenv("GITHUB_TOKEN")

# Vérifier que le token existe
if not token:
    raise Exception("Token GitHub manquant. Ajoutez GITHUB_TOKEN à un fichier .env.")

HEADERS = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github+json"
}

BASE_URL = "https://api.github.com/users"
OUTPUT_FILE = Path("data/users.json")
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

def get_users_batch(since):
    """Récupère une liste de 30 utilisateurs depuis l'API GitHub."""
    try:
        response = requests.get(f"{BASE_URL}?since={since}", headers=HEADERS)
        handle_rate_limit(response)
        response.raise_for_status()
        return response.json(), response.headers
    except requests.RequestException as e:
        print(f"[ERREUR] Requête get_users_batch échouée : {e}")
        return [], {}

def get_user_details(login):
    """Récupère les détails d'un utilisateur spécifique."""
    try:
        response = requests.get(f"{BASE_URL}/{login}", headers=HEADERS)
        handle_rate_limit(response)
        response.raise_for_status()
        data = response.json()
        return {
            "login": data.get("login"),
            "id": data.get("id"),
            "avatar_url": data.get("avatar_url"),
            "created_at": data.get("created_at"),
            "bio": data.get("bio"),
        }
    except requests.RequestException as e:
        print(f"[ERREUR] Détails utilisateur échoués pour {login} : {e}")
        return None

def handle_rate_limit(response):
    """Gère le quota de l'API GitHub."""
    remaining = int(response.headers.get("X-RateLimit-Remaining", 1))
    reset_time = int(response.headers.get("X-RateLimit-Reset", time.time() + 60))

    if remaining == 0:
        sleep_time = max(reset_time - int(time.time()), 0)
        print(f"[INFO] Quota atteint. Pause jusqu’à {time.ctime(reset_time)} ({sleep_time} sec)")
        time.sleep(sleep_time + 1)

def extract_users(max_users, since=0):
    """Extrait un nombre défini d'utilisateurs GitHub créés à partir de 2014."""
    all_users = []
    while len(all_users) < max_users:
        users_batch, headers = get_users_batch(since)
        if not users_batch:
            break

        for user in users_batch:
            if len(all_users) >= max_users:
                break

            login = user.get("login")
            user_details = get_user_details(login)
            if user_details:
                created_at = user_details.get("created_at")
                if created_at:
                    try:
                        created_date = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
                        if created_date.year >= 2014:
                            all_users.append(user_details)
                    except ValueError:
                        print(f"[ERREUR] Date invalide pour l'utilisateur {login} : {created_at}")
            time.sleep(0.5)

        since = users_batch[-1]["id"]

    return all_users

def save_to_json(users):
    """Sauvegarde les données utilisateurs dans un fichier JSON propre."""
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)
    print(f"[OK] {len(users)} utilisateurs enregistrés dans '{OUTPUT_FILE}'.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-users", type=int, default=60)
    parser.add_argument("--since", type=int, default=0)
    args = parser.parse_args()

    users = extract_users(args.max_users, since=args.since)
    save_to_json(users)

if __name__ == "__main__":
    main()
