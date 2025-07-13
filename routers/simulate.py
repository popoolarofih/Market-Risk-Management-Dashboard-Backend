from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
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

class StressTestResult(BaseModel):
    scenario: str
    result: Dict[str, Any]

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return user_id
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

def run_stress_test(portfolio_id: int):
    # Example stress test logic: apply a -10% shock to all assets
    assets_data = supabase.table("assets").select("*").eq("portfolio_id", portfolio_id).execute().data
    if not assets_data:
        return

    scenario = "Market Down 10%"
    result = {}
    for asset in assets_data:
        shocked_value = asset["quantity"] * 0.9  # Simulate a 10% drop
        result[asset["symbol"]] = {
            "original_quantity": asset["quantity"],
            "shocked_quantity": shocked_value,
            "asset_type": asset["asset_type"]
        }

    # Store the stress test result in the DB
    supabase.table("stress_tests").insert({
        "portfolio_id": portfolio_id,
        "scenario": scenario,
        "result": result
    }).execute()

@router.get("/portfolio/{id}/simulate", response_model=StressTestResult)
async def simulate_portfolio(id: int, background_tasks: BackgroundTasks, user_id: int = Depends(get_current_user)):
    # Retrieve latest stress test result for portfolio
    test_data = supabase.table("stress_tests").select("*").eq("portfolio_id", id).order("run_at", desc=True).limit(1).execute().data
    if not test_data:
        raise HTTPException(status_code=404, detail="Stress test result not found")
    
    background_tasks.add_task(run_stress_test, id)
    return StressTestResult(scenario=test_data[0]["scenario"], result=test_data[0]["result"])
