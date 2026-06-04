from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="AI Career Intelligence API")

# CORS (IMPORTANT for Streamlit connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema
class AnalyzeRequest(BaseModel):
    skills: str
    role: str
    country: str


@app.get("/")
def home():
    return {"status": "AI Career API Running 🚀"}


@app.post("/analyze")
def analyze(data: AnalyzeRequest):

    skills = data.skills.lower()
    role = data.role.lower()
    country = data.country.lower()

    score = 0
    matched = []

    # Skills logic
    if "talent acquisition" in skills:
        score += 20
        matched.append("Talent Acquisition")

    if "stakeholder" in skills:
        score += 15
        matched.append("Stakeholder Management")

    if "hrms" in skills:
        score += 15
        matched.append("HRMS")

    if "hris" in skills:
        score += 15
        matched.append("HRIS")

    if "erp" in skills:
        score += 10
        matched.append("ERP")

    if "powerbi" in skills or "power bi" in skills:
        score += 25
        matched.append("Power BI")

    if "sql" in skills:
        score += 15
        matched.append("SQL")

    # Role boost
    if "analyst" in role:
        score += 10

    if "hr" in role:
        score += 20

    if "data" in role:
        score += 15

    # Country boost
    if country == "usa":
        score += 10

    # Final decision
    if score >= 80:
        recommendation = "Excellent match for global HR / Analytics roles"
    elif score >= 60:
        recommendation = "Strong match for HR Analytics roles"
    elif score >= 40:
        recommendation = "Moderate match, needs upskilling"
    else:
        recommendation = "Needs significant upskilling"

    return {
        "input": data,
        "match_score": score,
        "matched_skills": matched,
        "recommendation": recommendation
    }


# Run locally (optional)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
