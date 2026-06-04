from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os

# -----------------------------
# APP INIT
# -----------------------------
app = FastAPI(
    title="AI Career SaaS",
    description="Live Job Market Intelligence using Adzuna API",
    version="1.0.0"
)

# -----------------------------
# CORS (ALLOW FRONTEND)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to Vercel URL in production
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
# LOAD API KEYS (SAFE FOR DEPLOYMENT)
# -----------------------------
APP_ID = os.getenv("ADZUNA_APP_ID", "YOUR_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY", "YOUR_APP_KEY")


# -----------------------------
# ROOT ENDPOINT (FIXES "NOT FOUND")
# -----------------------------
@app.get("/")
def home():
    return {
        "status": "AI Career SaaS Running 🚀",
        "message": "Backend is live",
        "docs": "/docs"
    }


# -----------------------------
# HEALTH CHECK
# -----------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# -----------------------------
# FETCH LIVE JOBS FROM ADZUNA
# -----------------------------
def fetch_jobs(skill: str, country: str):
    try:
        url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"

        params = {
            "app_id": APP_ID,
            "app_key": APP_KEY,
            "what": skill,
            "results_per_page": 10,
            "content-type": "application/json"
        }

        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        return data.get("results", [])

    except Exception as e:
        return []


# -----------------------------
# MAIN ANALYSIS ENDPOINT
# -----------------------------
@app.post("/analyze")
def analyze(data: AnalyzeRequest):

    skills_list = [s.strip() for s in data.skills.split(",") if s.strip()]

    total_jobs = 0
    breakdown = []

    for skill in skills_list:
        jobs = fetch_jobs(skill, data.country)

        total_jobs += len(jobs)

        breakdown.append({
            "skill": skill,
            "job_count": len(jobs),
            "top_jobs": [
                {
                    "title": job.get("title"),
                    "company": job.get("company", {}).get("display_name"),
                    "location": job.get("location", {}).get("display_name")
                }
                for job in jobs[:5]
            ]
        })

    # -----------------------------
    # REAL MARKET SCORE ENGINE
    # -----------------------------
    score = min(total_jobs * 5, 100)

    if score >= 80:
        recommendation = "🔥 Excellent market demand (High hiring activity)"
    elif score >= 50:
        recommendation = "📈 Good demand (Solid career path)"
    elif score >= 20:
        recommendation = "⚠️ Moderate demand (Upskill recommended)"
    else:
        recommendation = "❌ Low demand (Strong upskilling required)"

    # -----------------------------
    # RESPONSE
    # -----------------------------
    return {
        "input": data.dict(),
        "match_score": score,
        "total_jobs_found": total_jobs,
        "recommendation": recommendation,
        "skill_breakdown": breakdown,
        "data_source": "Adzuna Live API",
        "status": "success"
    }
