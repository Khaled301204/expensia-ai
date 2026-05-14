from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    PatternAnalysisRequest,
    PatternAnalysisResponse,
    ForecastRequest,
    ForecastResponse,
    CompleteInsightsRequest,
    CompleteInsightsResponse
)
from app.services.pattern_detection_service import PatternDetectionService
from app.services.forecasting_service import ForecastingService
from app.services.recommendation_service import RecommendationService

router = APIRouter()

# Initialize services
pattern_service = PatternDetectionService()
forecast_service = ForecastingService()
recommendation_service = RecommendationService()


@router.post("/analyze-patterns", response_model=PatternAnalysisResponse)
async def analyze_spending_patterns(request: PatternAnalysisRequest):
    """
    Analyze user's spending patterns
    
    Detects:
    - Temporal patterns (weekend overspending, payday spikes)
    - Behavioral patterns (favorite categories, spending days)
    - Anomalies (unusual transactions)
    - Trends (increasing/decreasing spending)
    """
    try:
        result = pattern_service.analyze_patterns(request.transactions)
        return PatternAnalysisResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pattern analysis error: {str(e)}")


@router.post("/forecast", response_model=ForecastResponse)
async def forecast_spending(request: ForecastRequest):
    """
    Forecast next month's spending by category
    
    Uses historical data to predict future spending patterns
    """
    try:
        result = forecast_service.forecast_next_month(request.historical_data)
        return ForecastResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Forecasting error: {str(e)}")


@router.post("/insights", response_model=CompleteInsightsResponse)
async def get_complete_insights(request: CompleteInsightsRequest):
    """
    Get complete financial insights in one call
    
    Combines:
    1. Pattern Detection - Spending behaviors and anomalies
    2. Forecasting - Next month predictions
    3. Recommendations - Actionable financial advice
    
    This is the main endpoint for dashboard/insights page
    """
    try:
        # 1. Analyze patterns
        patterns = pattern_service.analyze_patterns(request.transactions)
        
        # 2. Generate forecast (build historical data from transactions)
        historical_data = _build_historical_data(request.transactions)
        forecast = forecast_service.forecast_next_month(historical_data)
        
        # 3. Generate recommendations
        recommendations = recommendation_service.generate_recommendations(
            monthly_income=request.monthly_income,
            monthly_expenses=request.monthly_expenses,
            current_savings=request.current_savings,
            risk_preference=request.risk_preference,
            expense_breakdown=request.expense_breakdown,
            goals=request.goals
        )
        
        return CompleteInsightsResponse(
            success=True,
            patterns=PatternAnalysisResponse(**patterns),
            forecast=ForecastResponse(**forecast),
            recommendations=recommendations
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Insights error: {str(e)}")


def _build_historical_data(transactions: list) -> dict:
    """
    Convert transaction list to historical data format for forecasting
    
    Input: [
        {"date": "2026-01-15", "category": "Food & Dining", "amount": 150},
        {"date": "2026-01-20", "category": "Food & Dining", "amount": 200},
        {"date": "2026-02-10", "category": "Food & Dining", "amount": 180},
    ]
    
    Output: {
        "Food & Dining": [
            {"month": "2026-01", "amount": 350},
            {"month": "2026-02", "amount": 180}
        ]
    }
    """
    from collections import defaultdict
    from datetime import datetime
    
    # Group by category and month
    by_category_month = defaultdict(lambda: defaultdict(float))
    
    for t in transactions:
        try:
            date_str = t.get("date", "")
            if isinstance(date_str, str):
                date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            else:
                date_obj = date_str
            
            month_key = date_obj.strftime("%Y-%m")
            category = t.get("category", "Other")
            amount = float(t.get("amount", 0))
            
            by_category_month[category][month_key] += amount
        except:
            continue
    
    # Convert to required format
    historical_data = {}
    for category, months in by_category_month.items():
        monthly_list = [
            {"month": month, "amount": amount}
            for month, amount in sorted(months.items())
        ]
        historical_data[category] = monthly_list
    
    return historical_data