"use client";

import { useState } from "react";

export default function Home() {
  const [skills, setSkills] = useState("");
  const [role, setRole] = useState("");
  const [country, setCountry] = useState("us");
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
      alert("Backend connection failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main
      style={{
        maxWidth: "1200px",
        margin: "0 auto",
        padding: "40px",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <h1>🚀 AI Global Career Navigator</h1>

      <p>
        Live labor market intelligence powered by Adzuna + Groq AI
      </p>

      <div
        style={{
          display: "flex",
          gap: "10px",
          flexWrap: "wrap",
          marginTop: "20px",
        }}
      >
        <input
          placeholder="Skills (python, sql, power bi)"
          value={skills}
          onChange={(e) => setSkills(e.target.value)}
          style={{
            padding: "10px",
            width: "280px",
          }}
        />

        <input
          placeholder="Target Role"
          value={role}
          onChange={(e) => setRole(e.target.value)}
          style={{
            padding: "10px",
            width: "250px",
          }}
        />

        <select
          value={country}
          onChange={(e) => setCountry(e.target.value)}
          style={{
            padding: "10px",
            width: "220px",
          }}
        >
          <option value="us">United States</option>
          <option value="gb">United Kingdom</option>
          <option value="de">Germany</option>
          <option value="in">India</option>
          <option value="ca">Canada</option>
          <option value="au">Australia</option>
        </select>
      </div>

      <button
        onClick={analyzeCareer}
        disabled={loading}
        style={{
          marginTop: "20px",
          padding: "12px 24px",
          cursor: "pointer",
          borderRadius: "8px",
        }}
      >
        {loading ? "Analyzing..." : "Analyze Career Market"}
      </button>

      {result && (
        <>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit,minmax(220px,1fr))",
              gap: "20px",
              marginTop: "40px",
            }}
          >
            <div
              style={{
                border: "1px solid #ddd",
                borderRadius: "12px",
                padding: "20px",
              }}
            >
              <h3>📈 Market Score</h3>
              <h1>{result.market_data?.market_score}</h1>
            </div>

            <div
              style={{
                border: "1px solid #ddd",
                borderRadius: "12px",
                padding: "20px",
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
              gap: "20px",
              marginTop: "30px",
            }}
          >
            <div
              style={{
                border: "1px solid #ddd",
                borderRadius: "12px",
                padding: "20px",
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
                borderRadius: "12px",
                padding: "20px",
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
              marginTop: "30px",
              border: "1px solid #ddd",
              borderRadius: "12px",
              padding: "20px",
            }}
          >
            <h2>🔥 Top Job Titles</h2>

            <ul>
              {result.market_data?.top_job_titles?.map(
                (title: string, index: number) => (
                  <li key={index}>{title}</li>
                )
              )}
            </ul>
          </div>

          <div
            style={{
              marginTop: "30px",
              border: "1px solid #ddd",
              borderRadius: "12px",
              padding: "20px",
            }}
          >
            <h2>🤖 AI Career Strategy</h2>

            <pre
              style={{
                whiteSpace: "pre-wrap",
                fontFamily: "inherit",
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
