from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq
import requests
import os

load_dotenv()

app = FastAPI(title="AI Career SaaS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)


class AnalyzeRequest(BaseModel):
    skills: str
    role: str
    country: str


@app.get("/")
def health():
    return {"status": "AI Career SaaS Running 🚀"}


def get_jobs(skill, country):
    try:
        url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"

        params = {
            "app_id": ADZUNA_APP_ID,
            "app_key": ADZUNA_APP_KEY,
            "what": skill,
            "results_per_page": 20,
            "content-type": "application/json"
        }

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        if response.status_code != 200:
            return []

        data = response.json()

        return data.get("results", [])

    except Exception as e:
        print("Adzuna error:", e)
        return []


def generate_ai_insight(
    role,
    country,
    skills,
    total_jobs,
    top_companies,
    top_locations,
):
    try:

        prompt = f"""
You are an expert global career advisor.

Candidate Skills:
{skills}

Target Role:
{role}

Country:
{country}

Live Market Data:
Jobs Found: {total_jobs}

Top Hiring Companies:
{", ".join(top_companies)}

Top Hiring Locations:
{", ".join(top_locations)}

Create:

1. Market Demand Summary
2. Skill Gap Analysis
3. Top 5 Skills To Learn
4. Career Roadmap (90 Days)
5. Job Search Strategy
6. Resume Improvement Tips

Make it practical and professional.
"""

        completion = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior global career strategist."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1200
        )

        return completion.choices[0].message.content

    except Exception as e:
        print("Groq error:", e)
        return "AI insight unavailable."


@app.post("/analyze")
def analyze(data: AnalyzeRequest):

    skills = [s.strip() for s in data.skills.split(",")]

    total_jobs = 0

    companies = []
    locations = []

    skill_breakdown = []

    for skill in skills:

        jobs = get_jobs(skill, data.country)

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

            if company:
                companies.append(company)

            if location:
                locations.append(location)

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
                    ).get("display_name"),
                }
                for j in jobs[:5]
            ]
        })

    top_companies = list(
        dict.fromkeys(companies)
    )[:10]

    top_locations = list(
        dict.fromkeys(locations)
    )[:10]

    market_score = min(
        round(total_jobs * 2),
        100
    )

    ai_insight = generate_ai_insight(
        role=data.role,
        country=data.country,
        skills=data.skills,
        total_jobs=total_jobs,
        top_companies=top_companies,
        top_locations=top_locations,
    )

    return {
        "status": "success",
        "profile": {
            "skills": data.skills,
            "role": data.role,
            "country": data.country,
        },
        "market_data": {
            "market_score": market_score,
            "total_jobs_found": total_jobs,
            "top_companies": top_companies,
            "top_locations": top_locations,
        },
        "skill_breakdown": skill_breakdown,
        "ai_insight": ai_insight,
        "data_source": "Adzuna + Groq AI"
    }
