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

from typing import List

class RecommendationRequest(BaseModel):
    user_id: int
    monthly_income: float
    monthly_expenses: float
    current_savings: float
    risk_preference: str  # LOW, MEDIUM, HIGH
    expense_breakdown: dict  # {"Food & Dining": 3000, "Transport": 1500, ...}
    goals: Optional[List[dict]] = None  # [{"name": "iPhone", "target": 45000, "deadline": "2026-12-31"}]

class SpendingInsight(BaseModel):
    category: str
    current_spending: float
    average_spending: Optional[float] = None
    percentage_diff: Optional[float] = None
    insight: str
    recommendation: str

class SavingRecommendation(BaseModel):
    monthly_target: float
    breakdown: dict  # {"emergency_fund": 2000, "investments": 1000, ...}
    timeline_months: int
    recommendations: List[str]

class InvestmentSuggestion(BaseModel):
    type: str  # "MUTUAL_FUNDS", "GOLD", "BONDS", "SAVINGS_ACCOUNT"
    suggested_amount: float
    expected_return: str
    risk_level: str
    recommendation: str

class GoalPlan(BaseModel):
    goal_name: str
    target_amount: float
    current_amount: float
    monthly_saving_required: float
    months_to_goal: int
    feasibility: str  # "EASY", "MODERATE", "DIFFICULT"
    recommendation: str

class RecommendationResponse(BaseModel):
    success: bool
    spending_insights: List[SpendingInsight]
    saving_recommendations: SavingRecommendation
    investment_suggestions: List[InvestmentSuggestion]
    goal_plans: Optional[List[GoalPlan]] = None
    overall_score: float  # 0-100 financial health score