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

app = FastAPI(title="AI Career SaaS (Stable Version)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# ENV KEYS
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
# HEALTH CHECK
# -----------------------------
@app.get("/")
def home():
    return {"status": "backend running 🚀"}

# -----------------------------
# SAFE JOB FETCH (NO HANGS)
# -----------------------------
def fetch_jobs(skill, country):
    try:
        url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"

        params = {
            "app_id": APP_ID,
            "app_key": APP_KEY,
            "what": skill,
            "results_per_page": 5
        }

        res = requests.get(url, params=params, timeout=5)

        data = res.json()
        return data.get("results", [])

    except Exception as e:
        print("Job fetch error:", e)
        return []

# -----------------------------
# GROQ AI (FAST + SAFE)
# -----------------------------
def generate_ai_insight(prompt):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a career advisor. Give short, structured, practical advice."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:
        print("Groq error:", e)
        return "AI insight temporarily unavailable."

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
    # SIMPLE SCORE (NO HANG LOGIC)
    # -----------------------------
    score = min(total_jobs * 10, 100)

    # -----------------------------
    # FAST PROMPT (LIMIT TOKENS)
    # -----------------------------
    prompt = f"""
Skills: {data.skills}
Role: {data.role}
Country: {data.country}
Jobs found: {total_jobs}
Score: {score}

Give:
- Market demand
- Skill gap
- 3 next steps
- Job strategy
Keep it short.
"""

    ai_insight = generate_ai_insight(prompt)

    # -----------------------------
    # FINAL RESPONSE
    # -----------------------------
    return {
        "profile": {
            "skills": data.skills,
            "role": data.role,
            "country": data.country
        },
        "market_data": {
            "total_jobs_found": total_jobs,
            "market_score": score
        },
        "skill_breakdown": breakdown,
        "ai_insight": ai_insight,
        "status": "success"
    }
