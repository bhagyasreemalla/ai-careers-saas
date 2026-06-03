from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv()

app = FastAPI()

# CORS (IMPORTANT FOR DEPLOYMENT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GROQ CLIENT
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# INPUT MODEL
class UserInput(BaseModel):
    skills: str
    role: str
    country: str

@app.get("/")
def home():
    return {"status": "AI Career SaaS Running 🚀"}

@app.post("/analyze")
def analyze(data: UserInput):

    prompt = f"""
    You are a global HR AI assistant.

    Skills: {data.skills}
    Role: {data.role}
    Country: {data.country}

    Return JSON with:
    career_score (0-100),
    visa_score (0-100),
    competition,
    salary_range,
    missing_skills (list),
    top_countries (list),
    top_companies (list),
    jobs (list),
    roadmap (list),
    ai_insight (string)
    """

    response = client.chat.completions.create(
        model="model="llama-3.3-70b-versatile"",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "result": response.choices[0].message.content
    }
