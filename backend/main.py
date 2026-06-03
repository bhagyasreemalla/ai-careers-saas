from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class InputData(BaseModel):
    skills: str
    role: str
    country: str


@app.get("/")
def health():
    return {"status": "running"}


@app.post("/analyze")
def analyze(data: InputData):

    skills = data.skills.lower()

    required = ["python", "sql", "excel", "analytics"]

    missing = [s for s in required if s not in skills]
    score = (len(required) - len(missing)) * 25

    return {
        "match_score": score,
        "missing_skills": missing,
        "role": data.role,
        "country": data.country
    }
