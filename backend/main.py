from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
<<<<<<< HEAD

# CORS
=======
>>>>>>> a54e463 (fix cors for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
<<<<<<< HEAD
        "https://ai-careers-saas.onrender.com",
=======
        "https://ai-careers-saas.onrender.com"
>>>>>>> a54e463 (fix cors for frontend)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
<<<<<<< HEAD

=======
>>>>>>> a54e463 (fix cors for frontend)

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

        prompt = f"""
You are an expert global career advisor.

Skills: {data.skills}
Target Role: {data.role}
Country: {data.country}

Return ONLY valid JSON.

Use this exact structure:

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
Do not use ```json.
Return JSON only.
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

        try:
            return json.loads(result)
        except Exception:
            return {
                "raw_response": result
            }

    except Exception as e:
        return {
            "error": str(e)
        }