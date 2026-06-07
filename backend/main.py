from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class Input(BaseModel):
    skills: list
    experience_years: int
    target_role: str


BASE_SKILLS = {
    "People Analytics": ["Python", "SQL", "Statistics"],
    "HRIS Analyst": ["Workday", "SAP HCM"],
    "HR Analyst": ["Excel", "HR Basics"]
}


def ats_score(skills, role):
    required = BASE_SKILLS.get(role, ["Python", "SQL"])
    match = len(set(skills) & set(required))
    score = round((match / len(required)) * 100, 2)
    missing = list(set(required) - set(skills))
    return score, missing


def job_rank(skills):
    jobs = [
        {"title": "People Analytics", "skills": ["Python", "SQL"]},
        {"title": "HRIS Analyst", "skills": ["Workday", "SAP HCM"]},
        {"title": "HR Analyst", "skills": ["Excel", "HR Basics"]}
    ]

    results = []

    for j in jobs:
        match = len(set(skills) & set(j["skills"]))
        score = round((match / len(j["skills"])) * 100, 2)

        results.append({
            "title": j["title"],
            "score": score,
            "link": "https://www.linkedin.com/jobs"
        })

    return sorted(results, key=lambda x: x["score"], reverse=True)


def ai_insight(skills, role, score):
    prompt = f"""
You are an HR career advisor.

User skills: {skills}
Target role: {role}
ATS score: {score}

Give:
1. Career insight
2. 3 improvement steps
3. 1 job recommendation strategy
Return in JSON:
"""

    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
    )

    return res.choices[0].message.content


@app.post("/analyze")
def analyze(data: Input):

    score, missing = ats_score(data.skills, data.target_role)
    jobs = job_rank(data.skills)
    insight = ai_insight(data.skills, data.target_role, score)

    return {
        "ats_score": score,
        "missing_skills": missing,
        "job_matches": jobs,
        "ai_insight": insight
    }
