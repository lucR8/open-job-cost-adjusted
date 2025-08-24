# Job Market × Cost-of-Living — Pipeline & BI (Starter)

**Objectif :** agréger des offres d’emploi (quasi temps réel) et les ajuster au coût de la vie (loyers + inflation) pour classer les meilleures opportunités par territoire et métier.

## Démarrage rapide
1) Créez `.env` à partir de `.env.example`.
2) Lancez : `docker compose up -d --build`
3) Airflow : http://localhost:8080 (airflow/airflow) — DAG `ingest_offers_5min`
4) Metabase : http://localhost:3000
5) Postgres : localhost:5432 (db: warehouse / user: analytics / pw: analytics)

## Prochaines étapes
- Compléter l’endpoint exact de l’API France Travail dans `src/clients/france_travail.py`.
- Charger vos référentiels (loyers, IPC) dans `data/reference/`, les insérer en tables, et remplacer les modèles dbt de démonstration.
