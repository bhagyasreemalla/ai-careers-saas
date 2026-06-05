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

        response = requests.get(url, params=params, timeout=15)

        if response.status_code != 200:
            return []

        data = response.json()
        return data.get("results", [])

    except Exception as e:
        print("Adzuna Error:", str(e))
        return []
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

def generate_ai_insight(role, country, skills, total_jobs, companies, locations, titles, avg_salary, missing_skills):
    try:

        prompt = f"""
You are a senior global career strategist.

Candidate:
Skills: {skills}
Role: {role}
Country: {country}

Market Data:
Jobs Found: {total_jobs}
Average Salary: {avg_salary}

Top Companies:
{companies}

Top Locations:
{locations}

Top Job Titles:
{titles}

Missing Skills:
{missing_skills}

Give:
1. Market Demand
2. Career Outlook
3. Skill Gaps
4. Top Skills To Learn
5. 90-Day Roadmap
6. Resume Tips
7. Interview Strategy

Be practical and data-driven.
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a labor market expert."
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
        return f"Groq Error: {str(e)}"

# --------------------------------------------------
# ANALYZE
# --------------------------------------------------

@app.post("/analyze")
def analyze(data: AnalyzeRequest):

    skills = [
        s.strip()
        for s in data.skills.split(",")
        if s.strip()
    ]

    total_jobs = 0
    companies = []
    locations = []
    titles = []

    salary_values = []

    market_keywords = [
        "python", "sql", "power bi", "tableau",
        "aws", "azure", "snowflake", "excel",
        "sap", "workday"
    ]

    market_skill_count = {k: 0 for k in market_keywords}

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

            # -------- SALARY --------
            if job.get("salary_min"):
                salary_values.append(job.get("salary_min"))
            if job.get("salary_max"):
                salary_values.append(job.get("salary_max"))

            # -------- SKILL EXTRACTION --------
            desc = job.get("description", "").lower()

            for mk in market_keywords:
                if mk in desc:
                    market_skill_count[mk] += 1

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

    # -------- SALARY CALC --------
    avg_salary = 0
    if salary_values:
        avg_salary = round(sum(salary_values) / len(salary_values))

    # -------- MARKET SKILLS --------
    top_market_skills = sorted(
        market_skill_count.items(),
        key=lambda x: x[1],
        reverse=True
    )

    user_skills = [s.lower() for s in data.skills.split(",")]

    missing_skills = [
        k for k, v in top_market_skills[:5]
        if v > 0 and k not in user_skills
    ]

    market_score = min(int(total_jobs * 2), 100)

    ai_insight = generate_ai_insight(
        data.role,
        data.country,
        data.skills,
        total_jobs,
        top_companies,
        top_locations,
        top_titles,
        avg_salary,
        missing_skills
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

        "salary_data": {
            "average_salary": avg_salary
        },

        "market_skills": top_market_skills,

        "skill_gap_analysis": {
            "missing_skills": missing_skills
        },

        "skill_breakdown": skill_breakdown,

        "ai_insight": ai_insight,

        "data_source": "Live Adzuna + Groq"
    }
