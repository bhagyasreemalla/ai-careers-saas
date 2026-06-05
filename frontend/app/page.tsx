"use client";

import { useState } from "react";

export default function Home() {
  const [skills, setSkills] = useState("");
  const [role, setRole] = useState("");
  const [country, setCountry] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  async function analyzeCareer() {
    try {
      setLoading(true);

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
      alert("Backend connection failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main
      style={{
        maxWidth: "1200px",
        margin: "0 auto",
        padding: "40px",
        fontFamily: "Arial"
      }}
    >
      <h1>🚀 AI Global Career Navigator</h1>

      <p>
        Live labor market intelligence powered by Adzuna + Groq
      </p>

      <div
        style={{
          display: "flex",
          gap: 10,
          flexWrap: "wrap",
          marginTop: 20
        }}
      >
        <input
          placeholder="Skills (python, sql, power bi)"
          value={skills}
          onChange={(e) => setSkills(e.target.value)}
          style={{ padding: 10, width: 250 }}
        />

        <input
          placeholder="Target Role"
          value={role}
          onChange={(e) => setRole(e.target.value)}
          style={{ padding: 10, width: 250 }}
        />

        <input
          placeholder="Country (us, gb, de)"
          value={country}
          onChange={(e) => setCountry(e.target.value)}
          style={{ padding: 10, width: 180 }}
        />
      </div>

      <button
        onClick={analyzeCareer}
        disabled={loading}
        style={{
          marginTop: 20,
          padding: "12px 24px",
          cursor: "pointer",
        }}
      >
        {loading ? "Analyzing..." : "Analyze Career Market"}
      </button>

      {result && (
        <>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit,minmax(250px,1fr))",
              gap: 20,
              marginTop: 40
            }}
          >
            <div
              style={{
                border: "1px solid #ddd",
                borderRadius: 12,
                padding: 20
              }}
            >
              <h3>📈 Market Score</h3>
              <h1>{result.market_data?.market_score}</h1>
            </div>

            <div
              style={{
                border: "1px solid #ddd",
                borderRadius: 12,
                padding: 20
              }}
            >
              <h3>💼 Jobs Found</h3>
              <h1>{result.market_data?.total_jobs_found}</h1>
            </div>
          </div>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr",
              gap: 20,
              marginTop: 30
            }}
          >
            <div
              style={{
                border: "1px solid #ddd",
                borderRadius: 12,
                padding: 20
              }}
            >
              <h2>🏢 Top Hiring Companies</h2>

              <ul>
                {result.market_data?.top_companies?.map(
                  (company: string, index: number) => (
                    <li key={index}>{company}</li>
                  )
                )}
              </ul>
            </div>

            <div
              style={{
                border: "1px solid #ddd",
                borderRadius: 12,
                padding: 20
              }}
            >
              <h2>📍 Top Hiring Locations</h2>

              <ul>
                {result.market_data?.top_locations?.map(
                  (location: string, index: number) => (
                    <li key={index}>{location}</li>
                  )
                )}
              </ul>
            </div>
          </div>

          <div
            style={{
              marginTop: 30,
              border: "1px solid #ddd",
              borderRadius: 12,
              padding: 20
            }}
          >
            <h2>🤖 AI Career Strategy</h2>

            <pre
              style={{
                whiteSpace: "pre-wrap",
                fontFamily: "inherit"
              }}
            >
              {result.ai_insight}
            </pre>
          </div>
        </>
      )}
    </main>
  );
}
