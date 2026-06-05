"use client";

import { useState } from "react";

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
      const res = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ skills, role, country }),
      });

      const json = await res.json();
      setData(json);
    } catch (err) {
      alert("Backend not connected");
    }

    setLoading(false);
  };

  return (
    <div style={styles.page}>
      
      {/* LEFT SIDEBAR */}
      <div style={styles.sidebar}>
        <h2 style={{ color: "#0A66C2" }}>AI Career Navigator</h2>

        <input
          placeholder="Skills (python, sql)"
          value={skills}
          onChange={(e) => setSkills(e.target.value)}
          style={styles.input}
        />

        <input
          placeholder="Role"
          value={role}
          onChange={(e) => setRole(e.target.value)}
          style={styles.input}
        />

        <input
          placeholder="Country (us, uk, de)"
          value={country}
          onChange={(e) => setCountry(e.target.value)}
          style={styles.input}
        />

        <button onClick={analyze} style={styles.button}>
          {loading ? "Analyzing..." : "Run Market Analysis"}
        </button>
      </div>

      {/* MAIN DASHBOARD */}
      <div style={styles.main}>

        {!data && (
          <div style={styles.empty}>
            <h2>🚀 Career Intelligence Dashboard</h2>
            <p>Enter skills and run analysis to see real-time market insights</p>
          </div>
        )}

        {data && (
          <>
            {/* KPI CARDS */}
            <div style={styles.cardRow}>
              <Card title="Market Score" value={data.market_data.market_score} />
              <Card title="Jobs Found" value={data.market_data.total_jobs_found} />
              <Card title="Top Companies" value={data.market_data.top_companies.length} />
            </div>

            {/* CONTENT GRID */}
            <div style={styles.grid}>

              {/* LEFT: DATA */}
              <div style={styles.panel}>
                <h3>📊 Top Companies</h3>
                {data.market_data.top_companies.map((c: string, i: number) => (
                  <div key={i} style={styles.listItem}>{c}</div>
                ))}

                <h3 style={{ marginTop: 20 }}>📍 Locations</h3>
                {data.market_data.top_locations.map((l: string, i: number) => (
                  <div key={i} style={styles.listItem}>{l}</div>
                ))}

                <h3 style={{ marginTop: 20 }}>💼 Job Titles</h3>
                {data.market_data.top_job_titles.map((t: string, i: number) => (
                  <div key={i} style={styles.listItem}>{t}</div>
                ))}
              </div>

              {/* RIGHT: AI PANEL */}
              <div style={styles.aiPanel}>
                <h3>🤖 AI Career Copilot</h3>
                <pre style={styles.aiText}>
                  {data.ai_insight}
                </pre>
              </div>

            </div>
          </>
        )}
      </div>
    </div>
  );
}

/* ---------------- COMPONENT ---------------- */
function Card({ title, value }: any) {
  return (
    <div style={styles.card}>
      <h4>{title}</h4>
      <h2>{value}</h2>
    </div>
  );
}

/* ---------------- STYLES ---------------- */
const styles: any = {
  page: {
    display: "flex",
    height: "100vh",
    fontFamily: "Arial",
    background: "#f3f6f9",
  },

  sidebar: {
    width: "280px",
    padding: "20px",
    background: "white",
    borderRight: "1px solid #ddd",
    display: "flex",
    flexDirection: "column",
    gap: "10px",
  },

  input: {
    padding: "10px",
    border: "1px solid #ccc",
    borderRadius: "6px",
  },

  button: {
    marginTop: "10px",
    padding: "10px",
    background: "#0A66C2",
    color: "white",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer",
  },

  main: {
    flex: 1,
    padding: "20px",
    overflowY: "auto",
  },

  empty: {
    textAlign: "center",
    marginTop: "100px",
    color: "#666",
  },

  cardRow: {
    display: "flex",
    gap: "15px",
    marginBottom: "20px",
  },

  card: {
    flex: 1,
    background: "white",
    padding: "15px",
    borderRadius: "10px",
    boxShadow: "0 2px 5px rgba(0,0,0,0.05)",
  },

  grid: {
    display: "flex",
    gap: "20px",
  },

  panel: {
    flex: 1,
    background: "white",
    padding: "15px",
    borderRadius: "10px",
  },

  aiPanel: {
    flex: 1,
    background: "#0A66C2",
    color: "white",
    padding: "15px",
    borderRadius: "10px",
  },

  aiText: {
    whiteSpace: "pre-wrap",
    fontSize: "13px",
  },

  listItem: {
    padding: "6px 0",
    borderBottom: "1px solid #eee",
    fontSize: "14px",
  },
};
