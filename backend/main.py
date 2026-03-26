from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from engines.tax_calculator import calculate_tax_liability

app = FastAPI(title="ET Sentinel Backend")

# Setup CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class OptimizeRequest(BaseModel):
    salary: float
    hra: float = 0.0
    section_80c: float = 0.0

@app.post("/api/optimize")
async def optimize(request: OptimizeRequest):
    # Calculate real tax metrics using our engine
    tax_metrics = calculate_tax_liability(
        salary=request.salary, 
        hra=request.hra, 
        section_80c=request.section_80c
    )
    
    # Returns the dynamically calculated tax optimization and static portfolio analysis
    return {
        "tax_optimization": tax_metrics,
        "portfolio_analysis": {
            "total_aum": "₹16.2L",
            "leakage_detected": "₹2.8L",
            "overlap_percentage": "45%"
        }
    }
