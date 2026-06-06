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

# ==================================
# ENVIRONMENT
# ==================================
load_dotenv()

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

print("GROQ KEY FOUND:", bool(GROQ_API_KEY))

# ==================================
# APP
# ==================================
app = FastAPI(
    title="AI Global Career Navigator",
    version="saas-v4"
)

# ==================================
# CORS
# ==================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://ai-careers-saas.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================================
# TEMP DATABASE
# ==================================
db = {}

# ==================================
# REQUEST MODEL
# ==================================
class AnalyzeRequest(BaseModel):
    user_id: str | None = None
    skills: str
    role: str
    country: str

# ==================================
# HEALTH CHECK
# ==================================
@app.get("/")
def health():
    return {
        "status": "running",
        "version": "saas-v4"
    }

# ==================================
# ADZUNA
# ==================================
def get_jobs(skill: str, country: str):
    try:
        url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"

        params = {
            "app_id": ADZUNA_APP_ID,
            "app_key": ADZUNA_APP_KEY,
            "what": skill,
            "results_per_page": 20
        }

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        if response.status_code != 200:
            print("ADZUNA ERROR:", response.text)
            return []

        return response.json().get("results", [])

    except Exception as e:
        print("ADZUNA EXCEPTION:", str(e))
        return []

# ==================================
# AI INSIGHT
# ==================================
def generate_ai_insight(
    skills,
    role,
    total_jobs,
    companies
):
    try:

        prompt = f"""
You are an expert global career strategist.

Skills:
{skills}

Target Role:
{role}

Market Jobs Found:
{total_jobs}

Top Hiring Companies:
{companies[:5]}

Provide:

1. Career Summary
2. Skill Gap Analysis
3. 30-Day Roadmap
4. Hiring Probability

Keep it concise and practical.
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            messages=[
                {
                    "role": "system",
                    "content": "You are a world-class career advisor."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        print("GROQ ERROR:", str(e))
        return f"AI ERROR: {str(e)}"

# ==================================
# ANALYZE
# ==================================
@app.post("/analyze")
def analyze(data: AnalyzeRequest):

    skills = [
        s.strip()
        for s in data.skills.split(",")
        if s.strip()
    ]

    if not skills:
        return {
            "error": "No skills provided"
        }

    total_jobs = 0

    companies = []
    locations = []
    titles = []

    skill_breakdown = []

    for skill in skills:

        jobs = get_jobs(
            skill,
            data.country.lower()
        )

        total_jobs += len(jobs)

        for job in jobs:

            company = job.get(
                "company",
                {}
            ).get(
                "display_name",
                "Unknown"
            )

            location = job.get(
                "location",
                {}
            ).get(
                "display_name",
                "Unknown"
            )

            title = job.get(
                "title",
                "Unknown"
            )

            companies.append(company)
            locations.append(location)
            titles.append(title)

        skill_breakdown.append({
            "skill": skill,
            "job_count": len(jobs)
        })

    top_companies = [
        x[0]
        for x in Counter(companies).most_common(10)
    ]

    top_locations = [
        x[0]
        for x in Counter(locations).most_common(10)
    ]

    top_titles = [
        x[0]
        for x in Counter(titles).most_common(10)
    ]

    market_score = min(
        total_jobs * 2,
        100
    )

    hiring_probability = min(
        50 + (market_score // 2),
        95
    )

    ai_insight = generate_ai_insight(
        data.skills,
        data.role,
        total_jobs,
        top_companies
    )

    report_id = str(uuid4())

    user_id = data.user_id or "guest"

    report = {
        "report_id": report_id,
        "profile": data.dict(),
        "market_data": {
            "market_score": market_score,
            "hiring_probability": hiring_probability,
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
        "version": "saas-v4"
    }

# ==================================
# HISTORY
# ==================================
@app.get("/history/{user_id}")
def history(user_id: str):
    return {
        "user_id": user_id,
        "reports": db.get(user_id, [])
    }

# ==================================
# TEST ADZUNA
# ==================================
@app.get("/test-adzuna")
def test_adzuna():

    jobs = get_jobs(
        "python",
        "us"
    )

    return {
        "jobs_found": len(jobs),
        "sample_job": jobs[0] if jobs else None
    }
