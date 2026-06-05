from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq
from collections import Counter
from uuid import uuid4
import requests
import os
import time

# ----------------------------
# ENV
# ----------------------------
load_dotenv()

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

# ----------------------------
# APP
# ----------------------------
app = FastAPI(title="AI Global Career Navigator SaaS V3")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# SIMPLE IN-MEMORY DATABASE
# ----------------------------
db = {}

# ----------------------------
# REQUEST MODEL
# ----------------------------
class AnalyzeRequest(BaseModel):
    user_id: str | None = None
    skills: str
    role: str
    country: str

# ----------------------------
# HEALTH CHECK
# ----------------------------
@app.get("/")
def health():
    return {"status": "running", "version": "saas-v3"}

# ----------------------------
# ADZUNA API
# ----------------------------
def get_jobs(skill: str, country: str):
    try:
        url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"

        params = {
            "app_id": ADZUNA_APP_ID,
            "app_key": ADZUNA_APP_KEY,
            "what": skill,
            "results_per_page": 20
        }

        r = requests.get(url, params=params, timeout=10)

        if r.status_code != 200:
            return []

        return r.json().get("results", [])

    except:
        return []

# ----------------------------
# AI INSIGHT ENGINE
# ----------------------------
def generate_ai_insight(skills, role, total_jobs, companies):
    try:
        prompt = f"""
You are a senior career AI advisor.

Skills: {skills}
Role: {role}
Market Jobs: {total_jobs}
Top Companies: {companies[:5]}

Return:
- Career Summary
- Skill Gaps
- 30-Day Roadmap
- Hiring Probability
Keep it short and structured.
"""

        res = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You are a career strategist AI."},
                {"role": "user", "content": prompt}
            ]
        )

        return res.choices[0].message.content

    except:
        return "AI temporarily unavailable."

# ----------------------------
# ANALYZE API
# ----------------------------
@app.post("/analyze")
def analyze(data: AnalyzeRequest):

    skills = [s.strip() for s in data.skills.split(",") if s.strip()]

    if not skills:
        return {"error": "No skills provided"}

    total_jobs = 0
    companies, locations, titles = [], [], []

    skill_breakdown = []

    for skill in skills:
        jobs = get_jobs(skill, data.country.lower())
        total_jobs += len(jobs)

        for j in jobs:
            companies.append(j.get("company", {}).get("display_name", "Unknown"))
            locations.append(j.get("location", {}).get("display_name", "Unknown"))
            titles.append(j.get("title", "Unknown"))

        skill_breakdown.append({
            "skill": skill,
            "job_count": len(jobs)
        })

    top_companies = [x[0] for x in Counter(companies).most_common(10)]
    top_locations = [x[0] for x in Counter(locations).most_common(10)]
    top_titles = [x[0] for x in Counter(titles).most_common(10)]

    market_score = min(total_jobs * 2, 100)

    ai_insight = generate_ai_insight(
        data.skills,
        data.role,
        total_jobs,
        top_companies
    )

    # ----------------------------
    # SAAS V3: SAVE REPORT
    # ----------------------------
    report_id = str(uuid4())
    user_id = data.user_id or "guest"

    report = {
        "report_id": report_id,
        "profile": data.dict(),
        "market_data": {
            "market_score": market_score,
            "total_jobs_found": total_jobs,
            "top_companies": top_companies,
            "top_locations": top_locations,
            "top_job_titles": top_titles
        },
        "skill_breakdown": skill_breakdown,
        "ai_insight": ai_insight,
        "timestamp": time.time()
    }

    if user_id not in db:
        db[user_id] = []

    db[user_id].append(report)

    return {
        "status": "success",
        "report_id": report_id,
        "profile": data.dict(),
        "market_data": report["market_data"],
        "skill_breakdown": skill_breakdown,
        "ai_insight": ai_insight,
        "version": "saas-v3"
    }

# ----------------------------
# HISTORY API (SAAS FEATURE)
# ----------------------------
@app.get("/history/{user_id}")
def history(user_id: str):
    return {
        "user_id": user_id,
        "reports": db.get(user_id, [])
    }
