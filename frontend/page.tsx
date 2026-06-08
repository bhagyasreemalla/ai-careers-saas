"use client";

import { useState } from "react";
import axios from "axios";

export default function Home() {
  const [skills, setSkills] = useState("");
  const [role, setRole] = useState("");
  const [country, setCountry] = useState("");
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const analyze = async () => {
    setLoading(true);
    setData(null);

    try {
      const res = await axios.post("http://localhost:8000/analyze", {
        skills,
        role,
        country,
      });

      setData(res.data);
    } catch (err) {
      console.log(err);
      alert("Backend not reachable");
    }

    setLoading(false);
  };

  return (
    <div style={{ padding: 30, fontFamily: "Arial" }}>
      
      <h1 style={{ fontSize: 28, fontWeight: "bold" }}>
        🚀 AI Career Intelligence SaaS
      </h1>

      <p>Real-time job market + AI career advisor</p>

      <div style={{ marginTop: 20 }}>
        <input
          placeholder="Skills (python, sql)"
          value={skills}
          onChange={(e) => setSkills(e.target.value)}
          style={{ padding: 10, marginRight: 10 }}
        />

        <input
          placeholder="Role"
          value={role}
          onChange={(e) => setRole(e.target.value)}
          style={{ padding: 10, marginRight: 10 }}
        />

        <input
          placeholder="Country (us, de, in)"
          value={country}
          onChange={(e) => setCountry(e.target.value)}
          style={{ padding: 10 }}
        />
      </div>

      <button
        onClick={analyze}
        style={{
          marginTop: 20,
          padding: "10px 20px",
          background: "black",
          color: "white",
          cursor: "pointer",
        }}
      >
        {loading ? "Analyzing..." : "Analyze"}
      </button>

      {/* RESULTS */}
      {data && (
        <div style={{ marginTop: 30 }}>

          <h2>📊 Market Score: {data.market_data.market_score}</h2>
          <h3>Jobs Found: {data.market_data.total_jobs_found}</h3>

          <h2 style={{ marginTop: 20 }}>🤖 AI Insight</h2>
          <p>{data.ai_insight}</p>

          <h2 style={{ marginTop: 20 }}>📌 Skill Breakdown</h2>

          {data.skill_breakdown.map((s: any, i: number) => (
            <div key={i} style={{ marginBottom: 10 }}>
              <b>{s.skill}</b> — {s.job_count} jobs
            </div>
          ))}

        </div>
      )}
    </div>
  );
}