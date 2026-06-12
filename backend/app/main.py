from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the app directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api import quantum_risk, prompt, scanner, rsa, signature, report, chatbot, dashboard, risk_analyzer

app = FastAPI(title="QuantumShieldAI API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(quantum_risk.router, prefix="/api", tags=["Quantum Risk"])
app.include_router(prompt.router, prefix="/api", tags=["Prompt Purify"])
app.include_router(scanner.router, prefix="/api", tags=["Vulnerability Scanner"])
app.include_router(rsa.router, prefix="/api", tags=["RSA Encryption"])
app.include_router(signature.router, prefix="/api", tags=["Digital Signature"])
app.include_router(report.router, prefix="/api", tags=["Reports"])
app.include_router(chatbot.router, prefix="/api", tags=["Chatbot"])
app.include_router(dashboard.router, prefix="/api", tags=["Dashboard"])
app.include_router(risk_analyzer.router, prefix="/api", tags=["Risk Analyzer"])

# Serve homepage
@app.get("/")
async def read_root():
    homepage_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "homepage.html")
    if os.path.exists(homepage_path):
        return FileResponse(homepage_path)
    return {"message": "QuantumShieldAI API"}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "QuantumShieldAI is running"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
