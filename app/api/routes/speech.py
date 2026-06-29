from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from app.services.speech_service import SpeechService
from app.services.nlp_service import NLPService
from app.services.categorization_service import CategorizationService
from app.models.schemas import ExpenseParseResponse

router = APIRouter()

# Initialize services
speech_service = SpeechService()
nlp_service = NLPService()
categorization_service = CategorizationService()


@router.post("/speech-to-text")
async def transcribe_speech(
    audio: UploadFile = File(...),
    language: str = Form("auto")
):
    """
    Transcribe audio to text using OpenAI Whisper
    
    Supports:
    - ar: Arabic
    - en: English
    - auto: Automatic language detection
    
    Audio formats: WAV, MP3, FLAC, M4A, OGG, WEBM
    Max size: 25MB
    """
    try:
        # Read audio file
        audio_content = await audio.read()
        
        # Validate file size (max 25MB for Whisper)
        if len(audio_content) > 25 * 1024 * 1024:
            raise HTTPException(
                status_code=400, 
                detail="Audio file too large. Maximum size is 25MB"
            )
        
        # Transcribe
        result = speech_service.transcribe_audio(audio_content, language=language)
        
        if not result["success"]:
            raise HTTPException(
                status_code=400, 
                detail=result.get("error", "Transcription failed")
            )
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Speech recognition error: {str(e)}"
        )


@router.post("/speech-to-expense", response_model=ExpenseParseResponse)
async def speech_to_expense(
    audio: UploadFile = File(...),
    language: str = Form("auto")
):
    """
    Convert speech directly to expense data
    
    Complete flow:
    1. Transcribe audio to text (Whisper)
    2. Parse text to extract expense details (NLP)
    3. Categorize the expense (ML)
    4. Return structured data
    
    Example inputs:
    - Arabic: "دفعت 150 جنيه في ماكدونالدز"
    - English: "I spent 150 pounds on lunch at McDonald's"
    
    Returns structured expense with category
    """
    try:
        # Step 1: Transcribe audio
        audio_content = await audio.read()
        
        # Validate size
        if len(audio_content) > 25 * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail="Audio file too large. Maximum size is 25MB"
            )
        
        speech_result = speech_service.transcribe_audio(audio_content, language=language)
        
        if not speech_result["success"]:
            raise HTTPException(
                status_code=400, 
                detail=f"Transcription failed: {speech_result.get('error', 'Unknown error')}"
            )
        
        transcript = speech_result["transcript"]
        print("VOICE TRANSCRIPT:", transcript)
        
        # Step 2: Parse expense data from transcript
        parsed_data = nlp_service.parse_expense(transcript, language="en")
        print("PARSED DATA:", parsed_data)
        
        # Step 3: Categorize the expense
        category = None
        category_confidence = 0.0
        
        description = parsed_data.get("description", "")
        merchant = parsed_data.get("merchant", "")
        
        # Use description or merchant for categorization
        if description or merchant:
            categorization_result = categorization_service.categorize(
                description=description if description else transcript,
                merchant=merchant if merchant else ""
            )
            category = categorization_result["category"]
            category_confidence = categorization_result["confidence"]
        else:
            # Fallback: categorize the whole transcript
            categorization_result = categorization_service.categorize(
                description=transcript,
                merchant=""
            )
            category = categorization_result["category"]
            category_confidence = categorization_result["confidence"]
        
        # Build response
        expense_data = {
            "success": True,
            "amount": parsed_data.get("amount"),
            "merchant": parsed_data.get("merchant"),
            "description": parsed_data.get("description"),
            "date": parsed_data.get("date"),
            "category": category,
            "confidence": category_confidence,
            "speech_metadata": {
                "original_audio": audio.filename,
                "transcript": transcript,
                "confidence": speech_result["confidence"],
                "language": speech_result["language"],
                "detected_language": speech_result["detected_language"]
            }
        }
        
        return ExpenseParseResponse(**expense_data)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing speech: {str(e)}"
        )


@router.get("/supported-languages")
async def get_supported_languages():
    """
    Get list of supported languages for speech recognition
    """
    languages = speech_service.get_supported_languages()
    
    return {
        "languages": languages,
        "total": len(languages),
        "engine": "OpenAI Whisper",
        "cost": "FREE (unlimited)"
    }