import json
"""
filtered_users.py
Ce module permet de charger une liste d'utilisateurs GitHub depuis un fichier JSON, de supprimer les doublons, 
d'appliquer des filtres métier (présence de bio, d'avatar, et date de création postérieure à 2015), 
puis d'enregistrer la liste filtrée dans un nouveau fichier JSON.
Fonctions principales :
- load_users(filepath): Charge les utilisateurs depuis un fichier JSON.
- remove_duplicates(users): Supprime les doublons en se basant sur l'identifiant GitHub.
- is_valid_user(user): Vérifie si un utilisateur respecte les critères métier (bio, avatar, date).
- filter_users(users): Filtre la liste d'utilisateurs selon les critères métier.
- save_filtered_users(users, output_path): Enregistre les utilisateurs filtrés dans un fichier JSON propre.
- main(): Orchestration du processus de chargement, filtrage et sauvegarde.
Utilisation :
Exécuter ce script pour générer un fichier JSON contenant uniquement les utilisateurs valides et uniques.
"""
from pathlib import Path
from datetime import datetime

INPUT_PATH = Path("data/users.json")
OUTPUT_PATH = Path("data/filtered_users.json")


def load_users(filepath):
    """Charge les utilisateurs depuis un fichier JSON."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            users = json.load(f)
        print(f"[INFO] {len(users)} utilisateurs chargés depuis {filepath}")
        return users
    except Exception as e:
        print(f"[ERREUR] Échec de chargement : {e}")
        return []


def remove_duplicates(users):
    """Supprime les doublons en se basant sur l'identifiant GitHub."""
    unique_users = {}
    for user in users:
        uid = user.get("id")
        if uid:
            unique_users[uid] = user
    print(f"[INFO] Doublons supprimés : {len(users) - len(unique_users)}")
    return list(unique_users.values())


def is_valid_user(user):
    """Applique les filtres métier : bio, avatar, date >= 2015."""
    bio = user.get("bio")
    avatar = user.get("avatar_url")
    created_at = user.get("created_at")

    if not bio or not avatar or not created_at:
        return False

    try:
        created_date = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
        return created_date >= datetime(2015, 1, 1)
    except ValueError:
        return False


def filter_users(users):
    """Filtre les utilisateurs selon les critères métier."""
    filtered = [u for u in users if is_valid_user(u)]
    print(f"[INFO] Utilisateurs filtrés (post-2015, bio, avatar) : {len(filtered)}")
    return filtered


def save_filtered_users(users, output_path):
    """Enregistre les utilisateurs filtrés dans un fichier JSON propre."""
    to_save = [
        {
            "login": u["login"],
            "id": u["id"],
            "created_at": u["created_at"],
            "avatar_url": u["avatar_url"],
            "bio": u["bio"]
        }
        for u in users
    ]
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(to_save, f, indent=4, ensure_ascii=False)
    print(f"[OK] {len(to_save)} utilisateurs enregistrés dans {output_path}")


def main():
    raw_users = load_users(INPUT_PATH)
    unique_users = remove_duplicates(raw_users)
    filtered_users = filter_users(unique_users)
    save_filtered_users(filtered_users, OUTPUT_PATH)


if __name__ == "__main__":
    main()
