from pydantic import BaseModel
from typing import Optional, List

class CategorizeRequest(BaseModel):
    description: str
    merchant: Optional[str] = None
    amount: Optional[float] = None

class CategorizeResponse(BaseModel):
    success: bool
    category: str
    confidence: float
    alternative_categories: Optional[List[dict]] = None

class TrainingData(BaseModel):
    description: str
    merchant: Optional[str] = None
    category: str