from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
import sqlite3
import os

api_key = os.getenv("API_KEY")
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Replace with your Groq API Key
client = Groq(
api_key = os.getenv("API_KEY")
)

# ---------------- DATABASE ----------------

conn = sqlite3.connect("career.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS search_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    skills TEXT,
    role TEXT,
    country TEXT,
    ai_insight TEXT
)
""")

conn.commit()

# ---------------- INPUT MODEL ----------------

class UserInput(BaseModel):
    skills: str
    role: str
    country: str

# ---------------- JOBS ----------------

def get_jobs(role, country):
    return [
        f"{role} at Global Tech ({country}) - Visa Sponsored",
        f"Senior {role} Role in Fortune 500 ({country})",
        f"{role} Specialist Hiring in {country}"
    ]

# ---------------- AI ENGINE ----------------

def ai_insight(skills, role, country):

    prompt = f"""
You are an elite global mobility strategist.

User Skills: {skills}
Target Role: {role}
Target Country: {country}

Provide:

1. Why this country fits
2. Visa sponsorship strategy
3. Skill gaps
4. Top companies
5. 90-day roadmap
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content

# ---------------- ANALYZE ----------------

@app.post("/analyze")
def analyze(user: UserInput):

    ai_result = ai_insight(
        user.skills,
        user.role,
        user.country
    )

    cursor.execute(
        """
        INSERT INTO search_history
        (skills, role, country, ai_insight)
        VALUES (?, ?, ?, ?)
        """,
        (
            user.skills,
            user.role,
            user.country,
            ai_result
        )
    )

    conn.commit()

    return {
        "career_score": 78,
        "visa_score": 83,
        "competition": "Medium",
        "salary_range": "€55k - €85k",

        "missing_skills": [
            "Workday",
            "SQL",
            "Power BI",
            "People Analytics"
        ],

        "top_countries": [
            "Germany",
            "Netherlands",
            "Ireland",
            "Canada",
            "Australia"
        ],

        "top_companies": [
            "SAP",
            "Workday",
            "Siemens",
            "Bosch",
            "ASML"
        ],

        "jobs": get_jobs(
            user.role,
            user.country
        ),

        "roadmap": [
            "Week 1: Learn SQL",
            "Week 2: Build HR Analytics Project",
            "Week 3: Learn Workday Basics",
            "Week 4: Apply to 50 Roles"
        ],

        "ai_insight": ai_result
    }

# ---------------- HISTORY ----------------

@app.get("/history")
def history():

    cursor.execute("""
        SELECT *
        FROM search_history
        ORDER BY id DESC
        LIMIT 20
    """)

    rows = cursor.fetchall()

    return rows

# ---------------- HOME ----------------

@app.get("/")
def home():
    return {
        "status": "AI Global Career Navigator Running 🚀"
    }