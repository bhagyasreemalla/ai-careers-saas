from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq
from collections import Counter
import requests
import os

# ----------------------------
# ENV
# ----------------------------
load_dotenv()

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

print("GROQ KEY LOADED:", bool(GROQ_API_KEY))

# ----------------------------
# APP
# ----------------------------
app = FastAPI(title="AI Global Career Navigator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# GROQ CLIENT
# ----------------------------
client = Groq(api_key=GROQ_API_KEY)

# ----------------------------
# REQUEST MODEL
# ----------------------------
class AnalyzeRequest(BaseModel):
    skills: str
    role: str
    country: str

# ----------------------------
# HEALTH CHECK
# ----------------------------
@app.get("/")
def health():
    return {"status": "running"}

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

        response = requests.get(url, params=params, timeout=10)

        if response.status_code != 200:
            return []

        data = response.json()
        return data.get("results", [])

    except Exception as e:
        print("Adzuna error:", e)
        return []

# ----------------------------
# TEST ENDPOINT
# ----------------------------
@app.get("/test-adzuna")
def test_adzuna():
    jobs = get_jobs("python", "us")

    return {
        "jobs_found": len(jobs),
        "sample_job": jobs[0] if jobs else None
    }

# ----------------------------
# ANALYZE API
# ----------------------------
@app.post("/analyze")
def analyze(data: AnalyzeRequest):

    skills = [s.strip() for s in data.skills.split(",") if s.strip()]

    total_jobs = 0
    companies = []
    locations = []
    titles = []

    skill_breakdown = []

    for skill in skills:
        jobs = get_jobs(skill, data.country.lower())
        total_jobs += len(jobs)

        for job in jobs:
            company = job.get("company", {}).get("display_name")
            location = job.get("location", {}).get("display_name")
            title = job.get("title")

            if company:
                companies.append(company)
            if location:
                locations.append(location)
            if title:
                titles.append(title)

        skill_breakdown.append({
            "skill": skill,
            "job_count": len(jobs),
            "top_jobs": [
                {
                    "title": j.get("title"),
                    "company": j.get("company", {}).get("display_name"),
                    "location": j.get("location", {}).get("display_name")
                }
                for j in jobs[:5]
            ]
        })

    top_companies = [x[0] for x in Counter(companies).most_common(10)]
    top_locations = [x[0] for x in Counter(locations).most_common(10)]
    top_titles = [x[0] for x in Counter(titles).most_common(10)]

    market_score = min(total_jobs * 2, 100)

    return {
        "status": "success",
        "profile": data.dict(),
        "market_data": {
            "market_score": market_score,
            "total_jobs_found": total_jobs,
            "top_companies": top_companies,
            "top_locations": top_locations,
            "top_job_titles": top_titles
        },
        "skill_breakdown": skill_breakdown,
        "data_source": "Adzuna API"
    }
