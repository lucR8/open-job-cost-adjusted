from datetime import datetime
from pathlib import Path
import pandas as pd

def write_offers_parquet(df: pd.DataFrame, base_dir: str="data/raw/offers"):
    ts = datetime.utcnow()
    out_dir = Path(base_dir) / f"dt={ts.strftime('%Y-%m-%d')}" / f"hr={ts.strftime('%H')}"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "part-0000.parquet"
    df.to_parquet(out_path, index=False)
    return str(out_path)
