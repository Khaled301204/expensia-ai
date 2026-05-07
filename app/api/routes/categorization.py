from fastapi import APIRouter, HTTPException
from app.models.schemas import CategorizeRequest, CategorizeResponse, TrainingData
from app.services.categorization_service import CategorizationService

router = APIRouter()

# Initialize service (singleton)
categorization_service = CategorizationService()

@router.post("/categorize", response_model=CategorizeResponse)
async def categorize_expense(request: CategorizeRequest):
    """
    Categorize an expense using ML model
    
    Example request:
    {
        "description": "Lunch at Pizza Hut",
        "merchant": "Pizza Hut",
        "amount": 150.0
    }
    """
    try:
        result = categorization_service.categorize(
            description=request.description,
            merchant=request.merchant,
            amount=request.amount
        )
        
        return CategorizeResponse(
            success=True,
            category=result["category"],
            confidence=result["confidence"],
            alternative_categories=result["alternatives"]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Categorization error: {str(e)}")

@router.post("/train")
async def add_training_data(data: TrainingData):
    """
    Add new training data and retrain the model
    
    Example request:
    {
        "description": "Uber ride to work",
        "merchant": "Uber",
        "category": "Transportation"
    }
    """
    try:
        result = categorization_service.add_training_data(
            description=data.description,
            merchant=data.merchant or "",
            category=data.category
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training error: {str(e)}")

@router.get("/categories")
async def get_categories():
    """
    Get list of available categories
    """
    return {
        "categories": categorization_service.categories,
        "total": len(categorization_service.categories)
    }