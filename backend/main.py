from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

app = FastAPI()

# -----------------------------
# Input Schema
# -----------------------------
class InputData(BaseModel):
    skills: str
    role: str
    country: str


# -----------------------------
# Health Check (Render uses this)
# -----------------------------
@app.get("/")
def health():
    return {
        "status": "running",
        "message": "AI Career Navigator API is live 🚀"
    }


# -----------------------------
# Simple Skill Scoring Logic
# -----------------------------
def skill_score(skills: str):
    required = ["python", "sql", "excel", "analytics", "communication"]
    skills = skills.lower()
    return sum(1 for s in required if s in skills)


def missing_skills(skills: str):
    required = ["python", "sql", "excel", "analytics", "communication"]
    skills = skills.lower()
    return [s for s in required if s not in skills]


# -----------------------------
# OPTIONAL AI FUNCTION (SAFE)
# -----------------------------
def ai_insight(skills, role, country):
    """
    This only runs if OPENAI_API_KEY exists.
    If not, system falls back to rule-based logic.
    """

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return None

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)

        prompt = f"""
        You are a career advisor AI.

        User Skills: {skills}
        Target Role: {role}
        Country: {country}

        Return:
        - Match score (0-100)
        - Missing skills
        - Career advice
        - Learning roadmap
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

    except Exception as e:
        return None


# -----------------------------
# Main API Endpoint
# -----------------------------
@app.post("/analyze")
def analyze(data: InputData):

    try:
        score = skill_score(data.skills)
        missing = missing_skills(data.skills)

        ai_result = ai_insight(data.skills, data.role, data.country)

        return {
            "input": {
                "skills": data.skills,
                "role": data.role,
                "country": data.country
            },
            "rule_based": {
                "match_score": score * 20,
                "missing_skills": missing
            },
            "ai_insight": ai_result if ai_result else "AI not enabled (missing API key)",
            "status": "success"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
