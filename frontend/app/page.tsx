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
    } catch (err) {
      console.error(err);
      alert("Backend connection failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main style={{ maxWidth: 1000, margin: "auto", padding: 40 }}>
      <h1>🚀 AI Global Career Navigator</h1>

      <p>
        Real-time career intelligence powered by AI and live labor-market data.
      </p>

      <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
        <input
          placeholder="Skills (Python, SQL, Power BI)"
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
          style={{ padding: 10, width: 200 }}
        />
      </div>

      <button
        onClick={analyzeCareer}
        style={{
          marginTop: 20,
          padding: "12px 24px",
          cursor: "pointer",
        }}
      >
        {loading ? "Analyzing..." : "Analyze Career Market"}
      </button>

      {result && (
        <div style={{ marginTop: 40 }}>
          <h2>Career Analysis</h2>

          <pre
            style={{
              background: "#111",
              color: "#0f0",
              padding: 20,
              borderRadius: 10,
              overflow: "auto",
            }}
          >
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
    </main>
  );
}
