from celery import Celery
import os
from supabase import create_client, Client
from dotenv import load_dotenv
import numpy as np
from datetime import datetime

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

celery_app = Celery('tasks', broker='redis://localhost:6379/0')

def fetch_portfolio_assets(portfolio_id):
    assets_data = supabase.table("assets").select("*").eq("portfolio_id", portfolio_id).execute().data
    return assets_data

def fetch_market_prices(symbols):
    # Simulate market prices for demonstration (replace with real API)
    prices = {symbol: np.random.uniform(10, 100) for symbol in symbols}
    return prices

def compute_var_es(asset_values, confidence_level=0.95):
    # Simulate returns
    returns = np.random.normal(0, 0.02, (1000, len(asset_values)))
    portfolio_returns = returns.dot(np.array(asset_values) / sum(asset_values))
    var = -np.percentile(portfolio_returns, (1 - confidence_level) * 100) * sum(asset_values)
    es = -portfolio_returns[portfolio_returns <= -var].mean() * sum(asset_values)
    return float(var), float(es)

@celery_app.task
def calculate_risk(portfolio_id):
    assets = fetch_portfolio_assets(portfolio_id)
    if not assets:
        print(f"No assets found for portfolio {portfolio_id}")
        return False

    symbols = [asset["symbol"] for asset in assets]
    prices = fetch_market_prices(symbols)
    asset_values = [asset["quantity"] * prices[asset["symbol"]] for asset in assets]

    var, es = compute_var_es(asset_values)

    supabase.table("risk_metrics").insert({
        "portfolio_id": portfolio_id,
        "var": var,
        "es": es,
        "calculated_at": datetime.utcnow().isoformat()
    }).execute()

    print(f"Calculated VaR: {var}, ES: {es} for portfolio {portfolio_id}")
    return True
