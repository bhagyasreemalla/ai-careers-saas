from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
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


# SIMPLE REAL LOGIC (NOT AI)
def calculate_score(skills):
    base_skills = ["Python", "SQL", "Excel"]
    match = len(set(skills) & set(base_skills))
    return round((match / len(base_skills)) * 100, 2)


@app.post("/analyze")
def analyze(data: Input):

    # 1. SCORE (REAL LOGIC)
    ats_score = calculate_score(data.skills)

    # 2. MOCK JOBS (TEMPORARY)
    jobs = [
        {
            "title": "People Analytics Analyst",
            "score": 85,
            "link": "#"
        },
        {
            "title": "HRIS Analyst",
            "score": 75,
            "link": "#"
        }
    ]

    # 3. AI ONLY FOR INSIGHTS
    prompt = f"""
You are a career advisor.

User:
Skills: {data.skills}
Role: {data.target_role}
ATS Score: {ats_score}

Give:
- strengths
- weaknesses
- 3 action steps
"""

    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    insights = res.choices[0].message.content

    return {
        "ats_score": ats_score,
        "jobs": jobs,
        "insights": insights
    }
