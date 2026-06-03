from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ Fix frontend/backend connection issues
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# REQUEST MODEL
# -----------------------------
class AnalyzeRequest(BaseModel):
    skills: str
    role: str
    country: str

# -----------------------------
# ROOT (test if backend is alive)
# -----------------------------
@app.get("/")
def home():
    return {"status": "AI Global Career Navigator Running 🚀"}

# -----------------------------
# MAIN API ENDPOINT
# -----------------------------
@app.post("/analyze")
def analyze(data: AnalyzeRequest):
    
    skills = data.skills.lower()
    role = data.role.lower()

    # simple logic (replace with your AI/LLM later)
    score = 0

    if "python" in skills:
        score += 30
    if "sql" in skills:
        score += 20
    if "hr" in role:
        score += 30

    recommendation = "Strong match for HR Analytics roles" if score > 50 else "Needs upskilling"

    return {
        "input": data,
        "match_score": score,
        "recommendation": recommendation
    }
