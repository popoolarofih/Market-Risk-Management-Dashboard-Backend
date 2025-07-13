from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import portfolio, risk, simulate, auth

app = FastAPI(
    title="Market Risk Management Dashboard API",
    description="Backend API for Market Risk Management Dashboard",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(portfolio.router)
app.include_router(risk.router)
app.include_router(simulate.router)
