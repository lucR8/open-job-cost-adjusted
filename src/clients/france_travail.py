import os, time, requests
from typing import Dict, Iterator, Optional
from pydantic import BaseModel

FT_CLIENT_ID = os.getenv("FT_CLIENT_ID")
FT_CLIENT_SECRET = os.getenv("FT_CLIENT_SECRET")
FT_TOKEN_URL = os.getenv("FT_TOKEN_URL")
FT_API_BASE = (os.getenv("FT_API_BASE") or "").rstrip("/")

class Offer(BaseModel):
    id: str | None = None
    intitule: Optional[str] = None
    dateCreation: Optional[str] = None
    typeContrat: Optional[str] = None
    codeROME: Optional[str] = None
    lieuTravail: Optional[dict] = None
    salaire: Optional[dict] = None
    teletravail: Optional[str] = None

class FranceTravailClient:
    def __init__(self):
        if not (FT_CLIENT_ID and FT_CLIENT_SECRET and FT_TOKEN_URL and FT_API_BASE):
            raise RuntimeError("Env manquante. Renseignez .env")
        self._token = None
        self._exp = 0.0

    def _token_ok(self):
        return self._token and time.time() < self._exp - 60

    def _get_token(self) -> str:
        if self._token_ok(): return self._token
        data = {
            "grant_type": "client_credentials",
            "client_id": FT_CLIENT_ID,
            "client_secret": FT_CLIENT_SECRET,
            # "scope": os.getenv("FT_SCOPE",""),
        }
        r = requests.post(FT_TOKEN_URL, data=data, timeout=30)
        r.raise_for_status()
        p = r.json()
        self._token = p.get("access_token")
        self._exp = time.time() + int(p.get("expires_in", 1800))
        if not self._token:
            raise RuntimeError(f"Token KO: {p}")
        return self._token

    def iter_offers(self, params: Optional[Dict]=None) -> Iterator[Offer]:
        # ⚠️ Vérifiez le chemin exact dans la doc officielle : /offres/search ou autre
        url = f"{FT_API_BASE}/offres/search"
        page = 0
        while True:
            h = {"Authorization": f"Bearer {self._get_token()}"}
            q = dict(params or {}); q.update({"page": page})
            resp = requests.get(url, headers=h, params=q, timeout=30)
            if resp.status_code == 404:
                raise RuntimeError("Endpoint introuvable : adaptez FT_API_BASE et chemin /offres/search")
            resp.raise_for_status()
            data = resp.json()
            items = data.get("resultats") or data.get("offres") or []
            if not items: break
            for it in items:
                try: yield Offer.model_validate(it)
                except Exception: continue
            page += 1
