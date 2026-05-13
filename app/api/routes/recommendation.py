from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    RecommendationRequest, 
    RecommendationResponse,
    SpendingInsight,
    SavingRecommendation,
    InvestmentSuggestion,
    GoalPlan
)
from app.services.recommendation_service import RecommendationService

router = APIRouter()
recommendation_service = RecommendationService()

@router.post("/recommend", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    """
    Generate comprehensive financial recommendations
    
    Example request:
    {
        "user_id": 1,
        "monthly_income": 15000,
        "monthly_expenses": 8500,
        "current_savings": 50000,
        "risk_preference": "MEDIUM",
        "expense_breakdown": {
            "Food & Dining": 3000,
            "Transportation": 1500,
            "Shopping": 2000,
            "Entertainment": 1000,
            "Bills & Utilities": 1000
        },
        "goals": [
            {
                "name": "iPhone 15 Pro",
                "target_amount": 45000,
                "current_amount": 15000,
                "deadline": "2026-12-31"
            }
        ]
    }
    """
    try:
        result = recommendation_service.generate_recommendations(
            monthly_income=request.monthly_income,
            monthly_expenses=request.monthly_expenses,
            current_savings=request.current_savings,
            risk_preference=request.risk_preference,
            expense_breakdown=request.expense_breakdown,
            goals=request.goals
        )
        
        return RecommendationResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation error: {str(e)}")


@router.get("/benchmarks")
async def get_spending_benchmarks():
    """
    Get average spending benchmarks for all categories
    """
    return {
        "benchmarks": recommendation_service.spending_benchmarks,
        "currency": "EGP",
        "market": "Egypt"
    }