from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from .auth import oauth2_scheme
from jose import jwt
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

router = APIRouter()

class RiskMetrics(BaseModel):
    VaR: float
    ES: float

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return user_id
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

@router.get("/portfolio/{id}/risk", response_model=RiskMetrics)
async def get_risk_metrics(id: int, user_id: int = Depends(get_current_user)):
    # Retrieve risk metrics for portfolio
    risk_data = supabase.table("risk_metrics").select("*").eq("portfolio_id", id).execute().data
    if not risk_data:
        raise HTTPException(status_code=404, detail="Risk metrics not found")
    return RiskMetrics(VaR=risk_data[0]["var"], ES=risk_data[0]["es"])
