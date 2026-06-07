from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

# GROQ (AI)
from groq import Groq

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- GROQ CLIENT ----------------
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---------------- INPUT ----------------
class Input(BaseModel):
    skills: list
    experience_years: int
    target_role: str


# ---------------- ROLE DATABASE ----------------
ROLE_DB = {
    "People Analytics": ["Python", "SQL", "Statistics"],
    "HRIS Analyst": ["Workday", "SAP", "Excel"],
    "HR Analyst": ["Excel", "HR Basics", "Communication"]
}

JOBS = [
    {"title": "People Analytics", "skills": ["Python", "SQL"], "link": "https://linkedin.com/jobs"},
    {"title": "HRIS Analyst", "skills": ["Workday", "SAP"], "link": "https://linkedin.com/jobs"},
    {"title": "HR Analyst", "skills": ["Excel", "HR Basics"], "link": "https://linkedin.com/jobs"},
]

# ---------------- ATS SCORE ----------------
def ats_score(skills, role):
    required = ROLE_DB.get(role, ["Python", "SQL"])
    match = len(set(skills) & set(required))
    score = round((match / len(required)) * 100, 2)
    missing = list(set(required) - set(skills))
    return score, missing


# ---------------- JOB MATCH ----------------
def match_jobs(skills):
    results = []
    for job in JOBS:
        match = len(set(skills) & set(job["skills"]))
        score = round((match / len(job["skills"])) * 100, 2)

        results.append({
            "title": job["title"],
            "match_score": score,
            "link": job["link"]
        })

    return sorted(results, key=lambda x: x["match_score"], reverse=True)


# ---------------- AI INSIGHT (GROQ) ----------------
def ai_insight(skills, role, score):
    prompt = f"""
    You are a senior HR career coach AI.

    Candidate Skills: {skills}
    Target Role: {role}
    ATS Score: {score}

    Give:
    1. Career advice
    2. Skill gap improvement plan
    3. Job readiness verdict
    Keep it short and sharp.
    """

    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    return res.choices[0].message.content


# ---------------- ROOT ----------------
@app.get("/")
def root():
    return {"status": "V5 AI Career Copilot Running 🚀"}


# ---------------- MAIN API ----------------
@app.post("/analyze")
def analyze(data: Input):

    score, missing = ats_score(data.skills, data.target_role)
    jobs = match_jobs(data.skills)
    ai = ai_insight(data.skills, data.target_role, score)

    return {
        "ats_score": score,
        "missing_skills": missing,
        "job_matches": jobs,
        "ai_insight": ai
    }
