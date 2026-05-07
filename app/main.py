from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import categorization

app = FastAPI(
    title="Expensia AI Service",
    description="AI-powered expense analysis and categorization",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(categorization.router, prefix="/api", tags=["Categorization"])

@app.get("/")
def root():
    return {
        "message": "Expensia AI Service is running!",
        "version": "1.0.0",
        "status": "active",
        "features": {
            "categorization": "✅ Active",
            "speech_to_text": "⏳ Coming Soon",
            "forecasting": "⏳ Coming Soon"
        }
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "expensia-ai",
        "ml_model": "loaded"
    }