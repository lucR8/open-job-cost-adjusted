import pandas as pd
from src.clients.france_travail import FranceTravailClient
from src.utils.io import write_offers_parquet

def run():
    client = FranceTravailClient()
    rows = []
    for offer in client.iter_offers(params={"motsCles":"data","departement":"75"}):
        rows.append(offer.model_dump())
        if len(rows) >= 500: break
    if not rows:
        print("Aucune offre récupérée."); return
    df = pd.DataFrame(rows)
    path = write_offers_parquet(df)
    print(f"Ecrit: {path}")
