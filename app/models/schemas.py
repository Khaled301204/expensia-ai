from pydantic import BaseModel
from typing import Optional, List

# ========== CATEGORIZATION MODELS ==========

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


# ========== NLP PARSING MODELS ==========

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


# ========== SPEECH-TO-TEXT MODELS ========== (NEW)

class ExpenseParseResponse(BaseModel):
    """Response for parsed expense with optional speech metadata"""
    success: bool
    amount: Optional[float] = None
    merchant: Optional[str] = None
    description: Optional[str] = None
    date: Optional[str] = None
    category: Optional[str] = None
    confidence: Optional[float] = None
    speech_metadata: Optional[dict] = None  # Speech-to-text metadata


# ========== RECOMMENDATION MODELS ==========

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
    feasibility: str  # "EASY", "MODERATE", "DIFFICULT", "IMPOSSIBLE"
    recommendation: str

class RecommendationResponse(BaseModel):
    success: bool
    spending_insights: List[SpendingInsight]
    saving_recommendations: SavingRecommendation
    investment_suggestions: List[InvestmentSuggestion]
    goal_plans: Optional[List[GoalPlan]] = None
    overall_score: float  # 0-100 financial health score


# ========== PATTERN DETECTION MODELS ==========

class PatternAnalysisRequest(BaseModel):
    user_id: int
    transactions: List[dict]  # List of expense transactions

class TemporalPatterns(BaseModel):
    weekend_overspending: bool
    weekday_average: float
    weekend_average: float
    percentage_difference: float
    payday_spike: bool
    early_month_average: float
    late_month_average: float

class BehavioralPatterns(BaseModel):
    primary_spending_day: str
    primary_spending_category: str
    category_preferences: dict

class Anomaly(BaseModel):
    date: str
    category: str
    amount: float
    normal_amount: float
    reason: str

class TrendInfo(BaseModel):
    direction: str  # INCREASING, DECREASING, STABLE
    change_percentage: float
    insight: str

class PatternAnalysisResponse(BaseModel):
    success: bool
    temporal_patterns: TemporalPatterns
    behavioral_patterns: BehavioralPatterns
    anomalies: List[Anomaly]
    trends: dict  # category -> TrendInfo


# ========== FORECASTING MODELS ==========

class MonthlyData(BaseModel):
    month: str  # YYYY-MM
    amount: float

class ForecastRequest(BaseModel):
    user_id: int
    historical_data: dict  # category -> List[MonthlyData]

class CategoryForecast(BaseModel):
    predicted: float
    current_month: float
    trend: str  # UP, DOWN, STABLE
    change_percentage: float

class ForecastResponse(BaseModel):
    success: bool
    total_predicted: float
    by_category: dict  # category -> CategoryForecast
    confidence: float
    forecast_month: str


# ========== COMBINED INSIGHTS MODELS ==========

class CompleteInsightsRequest(BaseModel):
    user_id: int
    monthly_income: float
    monthly_expenses: float
    current_savings: float
    risk_preference: str
    expense_breakdown: dict
    transactions: List[dict]  # For pattern detection
    goals: Optional[List[dict]] = None

class CompleteInsightsResponse(BaseModel):
    success: bool
    patterns: PatternAnalysisResponse
    forecast: ForecastResponse
    recommendations: RecommendationResponse