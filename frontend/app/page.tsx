"use client";

import { useState } from "react";

export default function Home() {
  const [skills, setSkills] = useState("");
  const [role, setRole] = useState("");
  const [country, setCountry] = useState("Germany");
  const [result, setResult] = useState<any>(null);

  async function analyze() {
    try {
      const response = await fetch(
        "http://127.0.0.1:8000/analyze",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            skills,
            role,
            country,
          }),
        }
      );

      const data = await response.json();

      setResult(data);
    } catch (error) {
      alert("Backend connection failed");
      console.error(error);
    }
  }

  return (
    <div style={{ padding: 40 }}>
      <h1>🌍 AI Global Career Navigator</h1>

      <input
        placeholder="Skills"
        value={skills}
        onChange={(e) => setSkills(e.target.value)}
      />

      <br />
      <br />

      <input
        placeholder="Target Role"
        value={role}
        onChange={(e) => setRole(e.target.value)}
      />

      <br />
      <br />

      <select
        value={country}
        onChange={(e) => setCountry(e.target.value)}
      >
        <option>Germany</option>
        <option>Canada</option>
        <option>Ireland</option>
        <option>Netherlands</option>
      </select>

      <br />
      <br />

      <button onClick={analyze}>
        Analyze Career
      </button>

      {result && (
        <div style={{ marginTop: 30 }}>
          <h2>Career Score: {result.career_score}</h2>

          <h2>Visa Score: {result.visa_score}</h2>

          <h2>Competition: {result.competition}</h2>

          <h2>Salary: {result.salary_range}</h2>

          <h3>Missing Skills</h3>

          <ul>
            {result.missing_skills?.map(
              (skill: string, index: number) => (
                <li key={index}>{skill}</li>
              )
            )}
          </ul>

          <h3>AI Strategy</h3>

          <pre
            style={{
              whiteSpace: "pre-wrap",
            }}
          >
            {result.ai_insight}
          </pre>
        </div>
      )}
    </div>
  );
}