from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.categorization_service import CategorizationService
import csv
import json
from io import StringIO

router = APIRouter()
categorization_service = CategorizationService()


@router.post("/bulk-train")
async def bulk_train(file: UploadFile = File(...)):
    """
    Bulk train model from CSV or JSON file
    
    CSV format:
    description,merchant,category,amount
    lunch at McDonald's,McDonald's,Food & Dining,150
    
    JSON format:
    [
      {"description": "lunch", "merchant": "McDonald's", "category": "Food & Dining"},
      ...
    ]
    """
    try:
        content = await file.read()
        content_str = content.decode('utf-8')
        
        training_examples = []
        
        # Parse file
        if file.filename.endswith('.json'):
            training_examples = json.loads(content_str)
        elif file.filename.endswith('.csv'):
            csv_file = StringIO(content_str)
            reader = csv.DictReader(csv_file)
            training_examples = list(reader)
        else:
            raise HTTPException(400, "File must be .csv or .json")
        
        if not training_examples:
            raise HTTPException(400, "No training examples found")
        
        # Train on each example
        trained_count = 0
        failed_count = 0
        errors = []
        
        for i, example in enumerate(training_examples):
            try:
                # Call add_training_data method (changed from train)
                result = categorization_service.add_training_data(
                    description=example.get('description', ''),
                    merchant=example.get('merchant', ''),
                    category=example.get('category', '')
                )
                
                trained_count += 1
                
            except Exception as e:
                error_msg = f"Example {i}: {str(e)}"
                errors.append(error_msg)
                print(f"{ error_msg}")
                failed_count += 1
                
                # Show first 5 errors only
                if len(errors) <= 5:
                    print(f"   Data: {example}")
        
        # Print summary
        print(f"\n Training Summary:")
        print(f"   Total: {len(training_examples)}")
        print(f"   Trained: {trained_count}")
        print(f"   Failed: {failed_count}")
        
        if errors and len(errors) <= 10:
            print(f"\n Sample Errors:")
            for err in errors[:5]:
                print(f"   {err}")
        
        return {
            "success": trained_count > 0,
            "total_examples": len(training_examples),
            "trained": trained_count,
            "failed": failed_count,
            "message": f"Successfully trained model on {trained_count} examples",
            "sample_errors": errors[:5] if errors else []
        }
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(500, f"Bulk training failed: {str(e)}")


@router.get("/training-stats")
async def get_training_stats():
    """Get current model training statistics"""
    try:
        stats = categorization_service.get_model_stats()
        return {
            "success": True,
            "stats": stats
        }
    except:
        return {
            "success": True,
            "stats": {
                "message": "Stats not available - model needs training"
            }
        }