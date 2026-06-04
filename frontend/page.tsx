"use client";

import { useState } from "react";
import axios from "axios";

export default function Home() {
  const [skills, setSkills] = useState("");
  const [role, setRole] = useState("");
  const [country, setCountry] = useState("us");

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState("");

  const analyzeCareer = async () => {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await axios.post(
        "https://ai-career-saas.onrender.com/analyze",
        {
          skills,
          role,
          country,
        }
      );

      setResult(response.data);
    } catch (err) {
      setError("❌ Backend not reachable. Is FastAPI running?");
    }

    setLoading(false);
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>🚀 AI Career SaaS (LIVE Market Data)</h1>

      <p style={styles.subtitle}>
        Real-time job market insights powered by Adzuna API
      </p>

      <div style={styles.card}>
        <input
          style={styles.input}
          placeholder="Skills (e.g. Python, SQL, Power BI)"
          value={skills}
          onChange={(e) => setSkills(e.target.value)}
        />

        <input
          style={styles.input}
          placeholder="Role (e.g. Data Analyst)"
          value={role}
          onChange={(e) => setRole(e.target.value)}
        />

        <input
          style={styles.input}
          placeholder="Country (us, in, uk)"
          value={country}
          onChange={(e) => setCountry(e.target.value)}
        />

        <button style={styles.button} onClick={analyzeCareer}>
          {loading ? "Analyzing Live Market..." : "Analyze Career 🚀"}
        </button>

        {error && <p style={styles.error}>{error}</p>}
      </div>

      {result && (
        <div style={styles.resultCard}>
          <h2>📊 Match Score: {result.match_score}</h2>
          <h3>💡 {result.recommendation}</h3>
          <p>🔥 Total Jobs Found: {result.total_jobs_found}</p>

          <h3>📌 Skill Breakdown (Live Data)</h3>

          {result.skill_breakdown?.map((item: any, index: number) => (
            <div key={index} style={styles.skillBox}>
              <h4>🔹 {item.skill}</h4>
              <p>Jobs Found: {item.job_count}</p>

              <ul>
                {item.top_jobs?.map((job: any, i: number) => (
                  <li key={i}>
                    {job.title} — {job.company} ({job.location})
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

const styles: any = {
  container: {
    padding: 30,
    fontFamily: "Arial",
    background: "#0f172a",
    minHeight: "100vh",
    color: "white",
  },
  title: {
    fontSize: 32,
    fontWeight: "bold",
  },
  subtitle: {
    color: "#94a3b8",
    marginBottom: 20,
  },
  card: {
    background: "#1e293b",
    padding: 20,
    borderRadius: 12,
    maxWidth: 500,
  },
  input: {
    width: "100%",
    padding: 10,
    marginBottom: 10,
    borderRadius: 8,
    border: "none",
  },
  button: {
    width: "100%",
    padding: 12,
    background: "#38bdf8",
    border: "none",
    borderRadius: 8,
    cursor: "pointer",
    fontWeight: "bold",
  },
  resultCard: {
    marginTop: 20,
    padding: 20,
    background: "#111827",
    borderRadius: 12,
  },
  skillBox: {
    marginTop: 15,
    padding: 10,
    background: "#1f2937",
    borderRadius: 10,
  },
  error: {
    color: "red",
    marginTop: 10,
  },
};
