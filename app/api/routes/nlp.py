from fastapi import APIRouter, HTTPException
from app.models.schemas import ParseExpenseRequest, ParseExpenseResponse, ParsedExpenseData
from app.services.nlp_service import nlp_service

router = APIRouter()

@router.post("/parse-expense", response_model=ParseExpenseResponse)
async def parse_expense(request: ParseExpenseRequest):
    """
    Parse natural language text to extract expense information
    
    Example request:
    {
        "text": "I spent 150 pounds on lunch at Pizza Hut yesterday",
        "language": "en"
    }
    
    Example response:
    {
        "success": true,
        "parsed": {
            "amount": 150.0,
            "merchant": "Pizza Hut",
            "category": "food",
            "description": "lunch",
            "date": "2024-05-05",
            "confidence": {
                "amount": 0.99,
                "merchant": 0.92,
                "category": 0.75,
                "description": 0.85,
                "date": 0.88
            }
        },
        "original_text": "I spent 150 pounds on lunch at Pizza Hut yesterday"
    }
    """
    try:
        result = nlp_service.parse_expense(request.text, request.language)
        
        return ParseExpenseResponse(
            success=True,
            parsed=ParsedExpenseData(**result),
            original_text=request.text
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Parsing error: {str(e)}")


@router.post("/parse-and-categorize")
async def parse_and_categorize(request: ParseExpenseRequest):
    """
    Parse expense text AND categorize it in one call
    
    This combines NLP parsing with ML categorization for complete expense extraction
    """
    try:
        from app.services.categorization_service import CategorizationService
        
        # Parse the text
        parsed = nlp_service.parse_expense(request.text, request.language)
        
        # Prepare text for categorization
        # Use extracted description, merchant, or fallback to original text
        description_for_category = parsed.get("description") or parsed.get("merchant") or request.text
        merchant_for_category = parsed.get("merchant") or ""
        
        # Only categorize if we have something meaningful
        if description_for_category and description_for_category.strip():
            categorization_service = CategorizationService()
            
            category_result = categorization_service.categorize(
                description=description_for_category,
                merchant=merchant_for_category if merchant_for_category else None,
                amount=parsed.get("amount")
            )
            
            # Override the basic category hint with ML prediction
            parsed["category"] = category_result["category"]
            parsed["confidence"]["category"] = category_result["confidence"]
        else:
            # If we couldn't extract anything meaningful, use "Other"
            parsed["category"] = "Other"
            parsed["confidence"]["category"] = 0.5
        
        return {
            "success": True,
            "parsed": parsed,
            "original_text": request.text
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")