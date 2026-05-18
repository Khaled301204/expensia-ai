from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import categorization, nlp, recommendation, insights, speech, training

app = FastAPI(
    title="Expensia AI Service",
    description="AI-powered expense analysis and categorization with speech recognition",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(categorization.router, prefix="/api", tags=["Categorization"])
app.include_router(nlp.router, prefix="/api", tags=["NLP Parsing"])
app.include_router(recommendation.router, prefix="/api", tags=["Recommendations"])
app.include_router(insights.router, prefix="/api", tags=["Insights & Analytics"])
app.include_router(speech.router, prefix="/api", tags=["Speech-to-Text"])
app.include_router(training.router, prefix="/api", tags=["Training"])

@app.get("/")
def root():
    return {
        "message": "Expensia AI Service is running!",
        "version": "1.0.0",
        "status": "active",
        "features": {
            "categorization": "✅ Active (ML Model)",
            "nlp_parsing": "✅ Active",
            "recommendations": "✅ Active",
            "pattern_detection": "✅ Active",
            "forecasting": "✅ Active",
            "combined_insights": "✅ Active",
            "speech_to_text": "✅ Active (Whisper - FREE)"
        },
        "speech_engine": "OpenAI Whisper",
        "cost": "100% FREE (No limits)"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "expensia-ai",
        "ml_model": "loaded",
        "nlp_parser": "active",
        "recommendation_engine": "active",
        "pattern_detection": "active",
        "forecasting": "active",
        "speech_recognition": "active (Whisper)"
    }