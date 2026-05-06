from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Expensia AI Service",
    description="AI-powered expense analysis and categorization",
    version="1.0.0"
)

# CORS middleware - Allow Spring Boot backend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "Expensia AI Service is running!",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "expensia-ai",
        "python_version": "3.13.3"
    }

@app.get("/api/test")
def test_endpoint():
    return {
        "message": "Test endpoint working!",
        "available_features": [
            "Speech-to-Text (Coming Soon)",
            "Expense Categorization (Coming Soon)",
            "Forecasting (Coming Soon)"
        ]
    }
