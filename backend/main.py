from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="AI Career SaaS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    skills: str
    role: str
    country: str

@app.get("/")
def home():
    return {"status": "backend running 🚀"}

@app.post("/analyze")
def analyze(data: AnalyzeRequest):
    skills_list = [s.strip() for s in data.skills.split(",")]

    return {
        "profile": {
            "skills": data.skills,
            "role": data.role,
            "country": data.country
        },
        "market_data": {
            "total_jobs_found": 42,
            "market_score": 78
        },
        "skill_breakdown": [
            {
                "skill": skill,
                "job_count": 14,
                "top_jobs": [
                    {
                        "title": f"{data.role} Engineer",
                        "company": "Example Corp",
                        "location": data.country.upper()
                    }
                ]
            }
            for skill in skills_list
        ],
        "ai_insight": f"""
Market demand for {data.role} is strong.

Recommended next steps:
1. Strengthen {data.skills}
2. Build portfolio projects
3. Apply internationally

Country analyzed: {data.country}
""",
        "status": "success"
    }
