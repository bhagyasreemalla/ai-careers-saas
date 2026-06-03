from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

app = FastAPI(
    title="AI Global Career Navigator",
    version="1.0.0"
)


class UserInput(BaseModel):
    skills: str
    role: str
    country: str


@app.get("/")
def home():
    return {"status": "AI Career SaaS Running 🚀"}


@app.post("/analyze")
def analyze(data: UserInput):

    try:
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            return {
                "error": "GROQ_API_KEY not found"
            }

        client = Groq(api_key=api_key)

<<<<<<< HEAD
        prompt = f"""
You are an expert global career advisor.
=======
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
>>>>>>> 18e703b (fix: update deprecated Groq model)

Analyze the profile below and return ONLY valid JSON.

Skills: {data.skills}
Target Role: {data.role}
Country: {data.country}

Return this exact structure:

{{
  "career_score": 0,
  "visa_score": 0,
  "competition": "",
  "salary_range": "",
  "missing_skills": [],
  "top_countries": [],
  "top_companies": [],
  "jobs": [],
  "roadmap": [],
  "ai_insight": ""
}}

Do not use markdown.
Do not wrap the response in ```json.
Return only JSON.
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        result = response.choices[0].message.content.strip()

        # Convert AI JSON string to actual JSON object
        try:
            parsed = json.loads(result)
            return parsed
        except Exception:
            return {
                "raw_response": result
            }

    except Exception as e:
        return {
            "error": str(e)
        }
