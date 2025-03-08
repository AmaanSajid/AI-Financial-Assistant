# schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict

class StockData(BaseModel):
    symbol: str
    current_price: float
    pe_ratio: float
    market_cap: float
    volume: int
    last_updated: datetime = datetime.now()

class WebResearch(BaseModel):
    query: str
    top_results: List[Dict]
    summary: str

class FinancialAdvice(BaseModel):
    symbol: str
    analysis: str
