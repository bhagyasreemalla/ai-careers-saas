"use client";

import { useState } from "react";

export default function Home() {
  const [skills, setSkills] = useState("");
  const [role, setRole] = useState("");
  const [country, setCountry] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const analyzeCareer = async () => {
    try {
      setLoading(true);
      setResult(null);

      const response = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          skills,
          role,
          country,
        }),
      });

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error(error);
      alert("Cannot connect to backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main
      style={{
        padding: "40px",
        fontFamily: "Arial, sans-serif",
        maxWidth: "1000px",
        margin: "0 auto",
      }}
    >
      <h1>🚀 AI Career Navigator</h1>

      <p>
        Real-time career intelligence powered by AI and live job market data.
      </p>

      <div
        style={{
          display: "flex",
          gap: "10px",
          marginTop: "20px",
          flexWrap: "wrap",
        }}
      >
        <input
          placeholder="Skills (python, sql)"
          value={skills}
          onChange={(e) => setSkills(e.target.value)}
          style={{ padding: "10px", width: "250px" }}
        />

        <input
          placeholder="Target Role"
          value={role}
          onChange={(e) => setRole(e.target.value)}
          style={{ padding: "10px", width: "250px" }}
        />

        <input
          placeholder="Country Code (us, gb, de)"
          value={country}
          onChange={(e) => setCountry(e.target.value)}
          style={{ padding: "10px", width: "200px" }}
        />
      </div>

      <button
        onClick={analyzeCareer}
        disabled={loading}
        style={{
          marginTop: "20px",
          padding: "12px 24px",
          cursor: "pointer",
          border: "none",
          borderRadius: "8px",
        }}
      >
        {loading ? "Analyzing..." : "Analyze Career Market"}
      </button>

      {result && (
        <div style={{ marginTop: "40px" }}>
          <h2>📊 Market Analysis</h2>

          <div
            style={{
              display: "flex",
              gap: "20px",
              flexWrap: "wrap",
              marginTop: "20px",
            }}
          >
            <div
              style={{
                border: "1px solid #ccc",
                padding: "20px",
                borderRadius: "10px",
              }}
            >
              <h3>Market Score</h3>
              <p>{result.market_data?.market_score}</p>
            </div>

            <div
              style={{
                border: "1px solid #ccc",
                padding: "20px",
                borderRadius: "10px",
              }}
            >
              <h3>Jobs Found</h3>
              <p>{result.market_data?.total_jobs_found}</p>
            </div>
          </div>

          <h2 style={{ marginTop: "30px" }}>🤖 AI Career Insight</h2>

          <div
            style={{
              border: "1px solid #ccc",
              padding: "20px",
              borderRadius: "10px",
            }}
          >
            <pre
              style={{
                whiteSpace: "pre-wrap",
                fontFamily: "inherit",
              }}
            >
              {result.ai_insight}
            </pre>
          </div>

          <h2 style={{ marginTop: "30px" }}>📌 Skill Breakdown</h2>

          {result.skill_breakdown?.map((skill: any, index: number) => (
            <div
              key={index}
              style={{
                border: "1px solid #ccc",
                marginBottom: "20px",
                padding: "15px",
                borderRadius: "10px",
              }}
            >
              <h3>
                {skill.skill} ({skill.job_count} jobs)
              </h3>

              {skill.top_jobs?.map((job: any, idx: number) => (
                <div key={idx} style={{ marginTop: "10px" }}>
                  <strong>{job.title}</strong>
                  <br />
                  {job.company}
                  <br />
                  {job.location}
                </div>
              ))}
            </div>
          ))}
        </div>
      )}
    </main>
  );
}
