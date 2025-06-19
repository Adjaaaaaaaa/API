# API

├── extract_users.py               # Script d'extraction depuis l’API GitHub
├── filtered_users.py              # Script de filtrage métier
├── data/
│   ├── users.json                 # Données brutes extraites
│   └── filtered_users.json        # Données nettoyées et filtrées
├── api/
│   ├── main.py                    # Lancement de l’API FastAPI
│   ├── models.py                  # Schémas Pydantic
│   ├── routes.py                  # Endpoints API
│   ├── security.py                # Gestion de l’authentification
├── tests/
│   └── test_api.py                # Tests (facultatif)
├── requirements.txt              # Dépendances du projet
├── .env.example                  # Exemple de fichier d’environnement
└── README.md                     # Documentation complète du projet