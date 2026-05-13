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

class ParseExpenseRequest(BaseModel):
    text: str
    language: Optional[str] = "en"

class ParsedExpenseData(BaseModel):
    amount: Optional[float] = None
    merchant: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    date: Optional[str] = None
    confidence: dict

class ParseExpenseResponse(BaseModel):
    success: bool
    parsed: ParsedExpenseData
    original_text: str