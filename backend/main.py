from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Input(BaseModel):
    skills: list
    experience_years: int
    target_role: str


# -----------------------
# CORE LOGIC (NO AI YET)
# -----------------------

BASE_SKILLS = {
    "People Analytics": ["Python", "SQL", "Statistics"],
    "HRIS Analyst": ["Workday", "SAP HCM"],
    "HR Analyst": ["Excel", "HR Basics"]
}


def ats_score(skills, role):
    required = BASE_SKILLS.get(role, ["Python", "SQL"])
    match = len(set(skills) & set(required))
    return round((match / len(required)) * 100, 2), list(set(required) - set(skills))


def job_rank(skills):
    jobs = [
        {"title": "People Analytics", "skills": ["Python", "SQL"]},
        {"title": "HRIS Analyst", "skills": ["Workday", "SAP HCM"]},
        {"title": "HR Analyst", "skills": ["Excel", "HR Basics"]}
    ]

    results = []

    for j in jobs:
        match = len(set(skills) & set(j["skills"]))
        score = (match / len(j["skills"])) * 100

        results.append({
            "title": j["title"],
            "score": round(score, 2),
            "link": "#"
        })

    return sorted(results, key=lambda x: x["score"], reverse=True)


@app.post("/analyze")
def analyze(data: Input):

    score, missing = ats_score(data.skills, data.target_role)
    jobs = job_rank(data.skills)

    return {
        "ats_score": score,
        "missing_skills": missing,
        "job_matches": jobs
    }
