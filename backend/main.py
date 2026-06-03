from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# -----------------------------
# APP INIT
# -----------------------------
app = FastAPI(title="AI Global Career Navigator")

# -----------------------------
# CORS FIX (frontend connection)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# REQUEST MODEL
# -----------------------------
class AnalyzeRequest(BaseModel):
    skills: str
    role: str
    country: str

# -----------------------------
# ROOT CHECK
# -----------------------------
@app.get("/")
def home():
    return {"status": "AI Global Career Navigator Running 🚀"}

# -----------------------------
# CAREER ANALYSIS ENDPOINT
# -----------------------------
@app.post("/analyze")
def analyze(data: AnalyzeRequest):

    skills = data.skills.lower()
    role = data.role.lower()
    country = data.country.lower()

    score = 0
    matched_skills = []

    # -----------------------------
    # HR / Talent Domain Skills
    # -----------------------------
    if "talent acquisition" in skills:
        score += 20
        matched_skills.append("Talent Acquisition")

    if "stakeholder" in skills:
        score += 15
        matched_skills.append("Stakeholder Management")

    if "hrms" in skills:
        score += 15
        matched_skills.append("HRMS")

    if "hris" in skills:
        score += 15
        matched_skills.append("HRIS")

    if "erp" in skills:
        score += 10
        matched_skills.append("ERP Systems")

    # -----------------------------
    # Analytics / Tech Skills
    # -----------------------------
    if "powerbi" in skills or "power bi" in skills:
        score += 25
        matched_skills.append("Power BI")

    if "excel" in skills:
        score += 10
        matched_skills.append("Excel Analytics")

    if "sql" in skills:
        score += 15
        matched_skills.append("SQL")

    # -----------------------------
    # Role-based boost
    # -----------------------------
    if "analyst" in role:
        score += 10

    if "hr" in role:
        score += 20

    if "data" in role:
        score += 15

    # -----------------------------
    # Country boost (simple logic)
    # -----------------------------
    if country == "usa":
        score += 10
    elif country == "india":
        score += 5

    # -----------------------------
    # FINAL DECISION LOGIC
    # -----------------------------
    if score >= 80:
        recommendation = "Excellent match for Global HR / People Analytics roles"
    elif score >= 60:
        recommendation = "Strong match for HR Analytics roles"
    elif score >= 40:
        recommendation = "Moderate match, needs upskilling"
    else:
        recommendation = "Needs significant upskilling"

    # -----------------------------
    # RESPONSE
    # -----------------------------
    return {
        "input": data,
        "match_score": score,
        "matched_skills": matched_skills,
        "recommendation": recommendation
    }
