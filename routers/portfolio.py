from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
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

class Asset(BaseModel):
    symbol: str
    quantity: float
    asset_type: str

class PortfolioCreate(BaseModel):
    name: str
    assets: List[Asset]

class PortfolioOut(BaseModel):
    id: int
    name: str
    assets: List[Asset]

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return user_id
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

@router.post("/portfolio", response_model=PortfolioOut)
async def create_portfolio(portfolio: PortfolioCreate, user_id: int = Depends(get_current_user)):
    # Create portfolio
    result = supabase.table("portfolios").insert({
        "user_id": user_id,
        "name": portfolio.name
    }).execute()
    portfolio_id = result.data[0]["id"]
    # Add assets
    assets_payload = [
        {
            "portfolio_id": portfolio_id,
            "symbol": asset.symbol,
            "quantity": asset.quantity,
            "asset_type": asset.asset_type
        }
        for asset in portfolio.assets
    ]
    supabase.table("assets").insert(assets_payload).execute()
    return PortfolioOut(id=portfolio_id, name=portfolio.name, assets=portfolio.assets)

@router.get("/portfolio/{id}", response_model=PortfolioOut)
async def get_portfolio(id: int, user_id: int = Depends(get_current_user)):
    portfolio_data = supabase.table("portfolios").select("*").eq("id", id).execute().data
    if not portfolio_data:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    assets_data = supabase.table("assets").select("*").eq("portfolio_id", id).execute().data
    assets = [Asset(symbol=a["symbol"], quantity=a["quantity"], asset_type=a["asset_type"]) for a in assets_data]
    return PortfolioOut(id=id, name=portfolio_data[0]["name"], assets=assets)
