"use client";

import { useState } from "react";

export default function Home() {
  const [skills, setSkills] = useState("");
  const [role, setRole] = useState("");
  const [country, setCountry] = useState("");

  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const analyze = async () => {
    try {
      setLoading(true);
      setData(null);

      const res = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ skills, role, country }),
      });

      const json = await res.json();
      setData(json);
    } catch (err) {
      alert("Backend not reachable");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main style={styles.container}>
      <h1 style={styles.title}>🚀 AI Career SaaS Dashboard</h1>

      {/* INPUTS */}
      <div style={styles.inputRow}>
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
          placeholder="Country (us, gb, de)"
          value={country}
          onChange={(e) => setCountry(e.target.value)}
          style={styles.input}
        />

        <button onClick={analyze} style={styles.button}>
          {loading ? "Analyzing..." : "Analyze"}
        </button>
      </div>

      {/* KPI CARDS */}
      {data && (
        <div style={styles.cardsRow}>
          <Card title="Market Score" value={data.market_data?.market_score} />
          <Card title="Jobs Found" value={data.market_data?.total_jobs_found} />
          <Card title="Avg Salary" value={data.salary_data?.average_salary || 0} />
        </div>
      )}

      {/* MAIN GRID */}
      {data && (
        <div style={styles.grid}>
          {/* AI INSIGHT */}
          <div style={styles.panel}>
            <h2>🧠 AI Career Strategy</h2>
            <pre style={styles.pre}>{data.ai_insight}</pre>
          </div>

          {/* TOP COMPANIES */}
          <div style={styles.panel}>
            <h2>🏢 Top Companies</h2>
            {data.market_data?.top_companies?.map((c: string, i: number) => (
              <div key={i} style={styles.listItem}>{c}</div>
            ))}
          </div>

          {/* TOP LOCATIONS */}
          <div style={styles.panel}>
            <h2>📍 Locations</h2>
            {data.market_data?.top_locations?.map((l: string, i: number) => (
              <div key={i} style={styles.listItem}>{l}</div>
            ))}
          </div>

          {/* SKILL GAP */}
          <div style={styles.panel}>
            <h2>🎯 Skill Gap</h2>
            {data.skill_gap_analysis?.missing_skills?.map((s: string, i: number) => (
              <div key={i} style={styles.badge}>{s}</div>
            ))}
          </div>

          {/* MARKET SKILLS */}
          <div style={styles.panel}>
            <h2>📊 Market Skills</h2>
            {data.market_skills?.slice(0, 8).map((s: any, i: number) => (
              <div key={i} style={styles.skillBar}>
                <span>{s[0]}</span>
                <div style={{ ...styles.bar, width: `${Math.min(s[1] * 10, 100)}%` }} />
              </div>
            ))}
          </div>
        </div>
      )}
    </main>
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
  container: {
    padding: "30px",
    fontFamily: "Arial",
    background: "#f5f7fb",
    minHeight: "100vh",
  },

  title: {
    fontSize: "28px",
    marginBottom: "20px",
  },

  inputRow: {
    display: "flex",
    gap: "10px",
    flexWrap: "wrap",
    marginBottom: "20px",
  },

  input: {
    padding: "10px",
    borderRadius: "8px",
    border: "1px solid #ddd",
    width: "200px",
  },

  button: {
    padding: "10px 20px",
    background: "#111",
    color: "#fff",
    borderRadius: "8px",
    cursor: "pointer",
  },

  cardsRow: {
    display: "flex",
    gap: "15px",
    marginBottom: "20px",
  },

  card: {
    flex: 1,
    background: "#fff",
    padding: "15px",
    borderRadius: "10px",
    boxShadow: "0 2px 8px rgba(0,0,0,0.05)",
  },

  grid: {
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: "15px",
  },

  panel: {
    background: "#fff",
    padding: "15px",
    borderRadius: "10px",
    boxShadow: "0 2px 8px rgba(0,0,0,0.05)",
  },

  listItem: {
    padding: "6px 0",
    borderBottom: "1px solid #eee",
  },

  badge: {
    display: "inline-block",
    background: "#ffe8e8",
    padding: "6px 10px",
    margin: "5px",
    borderRadius: "6px",
  },

  skillBar: {
    marginBottom: "10px",
  },

  bar: {
    height: "6px",
    background: "#4f46e5",
    borderRadius: "5px",
    marginTop: "4px",
  },

  pre: {
    whiteSpace: "pre-wrap",
    fontSize: "13px",
  },
};
