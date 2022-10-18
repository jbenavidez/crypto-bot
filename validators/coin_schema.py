from typing import List, Optional
from pydantic import BaseModel, ValidationError, validator

class CoinValidator(BaseModel):
    name: str
    symbol: str
    current_price: float
    high_24h: float
    low_24h: float

