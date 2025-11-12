from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel, Field, condecimal
from typing import Dict, List, Optional
from uuid import uuid4

app = FastAPI(title="Orders API")
DB: Dict[str, Dict] = {}
ETAG: Dict[str, str] = {}  # naive per-resource version

class OrderIn(BaseModel):
    user_id: str = Field(min_length=1)
    amount: condecimal(gt=0, max_digits=10, decimal_places=2)
    currency: str = Field(pattern="^[A-Z]{3}$")

class OrderOut(OrderIn):
    id: str
    status: str

def _etag() -> str:
    return uuid4().hex[:8]

def _require_auth(token: Optional[str]):
    if token != "Bearer demo-token":
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.post("/orders", response_model=OrderOut, status_code=201)
def create_order(order: OrderIn, authorization: Optional[str] = Header(None)):
    _require_auth(authorization)
    oid = uuid4().hex[:12]
    rec = { "id": oid, "status": "PENDING", **order.model_dump() }
    DB[oid] = rec
    ETAG[oid] = _etag()
    return rec

@app.get("/orders/{oid}", response_model=OrderOut)
def get_order(oid: str, authorization: Optional[str] = Header(None)):
    _require_auth(authorization)
    if oid not in DB: raise HTTPException(404, "Not found")
    return DB[oid]

@app.put("/orders/{oid}", response_model=OrderOut)
def update_order(
    oid: str,
    order: OrderIn,
    authorization: Optional[str] = Header(None),
    if_match: Optional[str] = Header(None)
):
    _require_auth(authorization)
    if oid not in DB: raise HTTPException(404, "Not found")
    if if_match is None or if_match != ETAG[oid]:
        raise HTTPException(status_code=412, detail="Precondition Failed: stale or missing ETag")
    rec = { "id": oid, "status": "PENDING", **order.model_dump() }
    DB[oid] = rec
    ETAG[oid] = _etag()
    return rec

@app.get("/orders", response_model=List[OrderOut])
def list_orders(limit: int = 10, offset: int = 0, authorization: Optional[str] = Header(None)):
    _require_auth(authorization)
    items = list(DB.values())
    return items[offset: offset + min(limit, 50)]  # cap limit at 50
