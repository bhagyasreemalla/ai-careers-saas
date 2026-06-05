from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq
from collections import Counter
import requests
import os

# --------------------------------------------------
# ENV
# --------------------------------------------------

load_dotenv()
print("GROQ KEY FOUND:", bool(os.getenv("GROQ_API_KEY")))

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# --------------------------------------------------
# APP
# --------------------------------------------------

app = FastAPI(
    title="AI Global Career Navigator",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# GROQ
# --------------------------------------------------

client = Groq(api_key=GROQ_API_KEY)

# --------------------------------------------------
# MODEL
# --------------------------------------------------

class AnalyzeRequest(BaseModel):
    skills: str
    role: str
    country: str

# --------------------------------------------------
# HEALTH
# --------------------------------------------------

@app.get("/")
def health():
    return {
        "status": "running",
        "service": "AI Global Career Navigator"
    }

# --------------------------------------------------
# ADZUNA
# --------------------------------------------------

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
            timeout=15
        )

        if response.status_code != 200:
            print("Adzuna status:", response.status_code)
            return []

        data = response.json()

        return data.get("results", [])

    except Exception as e:
        print("Adzuna Error:", str(e))
        return []

# --------------------------------------------------
# TEST ADZUNA
# --------------------------------------------------

@app.get("/test-adzuna")
def test_adzuna():

    jobs = get_jobs("python", "us")

    return {
        "jobs_found": len(jobs),
        "sample_job": jobs[0] if jobs else None
    }

# --------------------------------------------------
# AI
# --------------------------------------------------

def generate_ai_insight(
    role,
    country,
    skills,
    total_jobs,
    companies,
    locations,
    titles
):

    try:

        prompt = f"""
You are a senior global labor market analyst.

Candidate Profile:
Skills: {skills}
Role: {role}
Country: {country}

Live Market Data:

Jobs Found:
{total_jobs}

Top Companies:
{companies}

Top Locations:
{locations}

Top Job Titles:
{titles}

Provide:

1. Market Demand Score Explanation
2. Career Outlook
3. Skill Gaps
4. Top 5 Skills To Learn
5. 90-Day Career Roadmap
6. Resume Recommendations
7. Interview Preparation Tips

Use bullet points.
Use market data.
Avoid generic advice.
"""

        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a labor market intelligence expert."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.5,
            max_tokens=1200
        )

        return response.choices[0].message.content

    except Exception as e:

        print("===================================")
        print("GROQ ERROR:")
        print(str(e))
        print("===================================")

        return str(e)

# --------------------------------------------------
# ANALYZE
# --------------------------------------------------

@app.post("/analyze")
def analyze(data: AnalyzeRequest):

    print("COUNTRY RECEIVED:", data.country)
    skills = [
        s.strip()
        for s in data.skills.split(",")
        if s.strip()
    ]

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

            company = (
                job.get("company", {})
                .get("display_name")
            )

            location = (
                job.get("location", {})
                .get("display_name")
            )

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
                    "company": j.get(
                        "company",
                        {}
                    ).get("display_name"),
                    "location": j.get(
                        "location",
                        {}
                    ).get("display_name")
                }
                for j in jobs[:5]
            ]
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
        int(total_jobs * 2),
        100
    )

    ai_insight = generate_ai_insight(
        role=data.role,
        country=data.country,
        skills=data.skills,
        total_jobs=total_jobs,
        companies=top_companies,
        locations=top_locations,
        titles=top_titles
    )

    return {
        "status": "success",

        "profile": {
            "skills": data.skills,
            "role": data.role,
            "country": data.country
        },

        "market_data": {
            "market_score": market_score,
            "total_jobs_found": total_jobs,
            "top_companies": top_companies,
            "top_locations": top_locations,
            "top_job_titles": top_titles
        },

        "skill_breakdown": skill_breakdown,

        "ai_insight": ai_insight,

        "data_source": "Live Adzuna + Groq"
    }
