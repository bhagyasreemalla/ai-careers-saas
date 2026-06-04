from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
from groq import Groq

# -----------------------------
# INIT
# -----------------------------
load_dotenv()

app = FastAPI(title="AI Career SaaS v2 (Groq Powered)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# KEYS
# -----------------------------
APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

# -----------------------------
# INPUT MODEL
# -----------------------------
class AnalyzeRequest(BaseModel):
    skills: str
    role: str
    country: str

# -----------------------------
# HOME
# -----------------------------
@app.get("/")
def home():
    return {"status": "AI Career SaaS (Groq + Adzuna) running 🚀"}

# -----------------------------
# FETCH JOBS
# -----------------------------
def fetch_jobs(skill, country):
    try:
        url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"
        params = {
            "app_id": APP_ID,
            "app_key": APP_KEY,
            "what": skill,
            "results_per_page": 10
        }

        res = requests.get(url, params=params, timeout=10)
        return res.json().get("results", [])

    except:
        return []

# -----------------------------
# GROQ AI ENGINE
# -----------------------------
def generate_ai_insight(prompt):

    try:
        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a world-class career advisor. Give structured, crisp, actionable insights."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI insight failed: {str(e)}"

# -----------------------------
# MAIN API
# -----------------------------
@app.post("/analyze")
def analyze(data: AnalyzeRequest):

    skills = [s.strip() for s in data.skills.split(",")]

    total_jobs = 0
    breakdown = []

    for skill in skills:
        jobs = fetch_jobs(skill, data.country)
        total_jobs += len(jobs)

        breakdown.append({
            "skill": skill,
            "job_count": len(jobs),
            "top_jobs": [
                {
                    "title": j.get("title"),
                    "company": j.get("company", {}).get("display_name"),
                    "location": j.get("location", {}).get("display_name")
                }
                for j in jobs[:3]
            ]
        })

    # -----------------------------
    # SCORE ENGINE
    # -----------------------------
    score = min(total_jobs * 6, 100)

    # -----------------------------
    # GROQ PROMPT
    # -----------------------------
    prompt = f"""
User Profile:
Skills: {data.skills}
Role: {data.role}
Country: {data.country}

Market Data:
Total Jobs Found: {total_jobs}
Market Score: {score}

Break down:
1. Market demand
2. Skill gaps
3. What to learn next (step-by-step roadmap)
4. Job targeting strategy
5. One motivational insight
"""

    ai_insight = generate_ai_insight(prompt)

    # -----------------------------
    # FINAL RESPONSE (SAA S LEVEL)
    # -----------------------------
    return {
        "profile": {
            "skills": data.skills,
            "role": data.role,
            "country": data.country
        },
        "market_data": {
            "total_jobs_found": total_jobs,
            "market_score": score,
            "status": "Live Adzuna Data"
        },
        "skill_breakdown": breakdown,
        "ai_insight": ai_insight,
        "engine": "Groq (LLaMA 3.1)",
        "status": "success"
    }
