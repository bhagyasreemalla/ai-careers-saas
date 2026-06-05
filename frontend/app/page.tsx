"use client";

import { useState } from "react";

export default function Home() {
  const [skills, setSkills] = useState("");
  const [role, setRole] = useState("");
  const [country, setCountry] = useState("");
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const API_URL =
    process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  const analyze = async () => {
    setLoading(true);
    setData(null);

    try {
      const res = await fetch(`${API_URL}/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          skills,
          role,
          country,
          user_id: "demo-user-1"
        }),
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
      {/* SIDEBAR */}
      <div style={styles.sidebar}>
        <h2 style={styles.logo}>AI Career Navigator</h2>

        <input
          placeholder="Skills"
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
          placeholder="Country (us, in, uk)"
          value={country}
          onChange={(e) => setCountry(e.target.value)}
          style={styles.input}
        />

        <button onClick={analyze} style={styles.button} disabled={loading}>
          {loading ? "Analyzing..." : "Run Analysis"}
        </button>
      </div>

      {/* MAIN */}
      <div style={styles.main}>
        {!data && !loading && (
          <div style={styles.empty}>
            <h1>🚀 AI Career Intelligence SaaS</h1>
            <p>Analyze jobs, skills & career opportunities instantly</p>
          </div>
        )}

        {loading && (
          <div style={styles.loading}>
            <div style={styles.spinner}></div>
            <p>Analyzing job market...</p>
          </div>
        )}

        {data && (
          <>
            {/* CARDS */}
            <div style={styles.cards}>
              <Card title="Market Score" value={data.market_data.market_score} />
              <Card title="Jobs Found" value={data.market_data.total_jobs_found} />
              <Card title="Companies" value={data.market_data.top_companies.length} />
            </div>

            <div style={styles.grid}>
              {/* LEFT */}
              <div style={styles.panel}>
                <h3>Top Companies</h3>
                {data.market_data.top_companies.map((c: string, i: number) => (
                  <div key={i} style={styles.item}>{c}</div>
                ))}

                <h3>Locations</h3>
                {data.market_data.top_locations.map((l: string, i: number) => (
                  <div key={i} style={styles.item}>{l}</div>
                ))}

                <h3>Job Titles</h3>
                {data.market_data.top_job_titles.map((t: string, i: number) => (
                  <div key={i} style={styles.item}>{t}</div>
                ))}
              </div>

              {/* AI */}
              <div style={styles.ai}>
                <h3>AI Career Copilot</h3>
                <div style={styles.aiText}>{data.ai_insight}</div>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

/* CARD */
function Card({ title, value }: any) {
  return (
    <div style={styles.card}>
      <h4>{title}</h4>
      <h2>{value}</h2>
    </div>
  );
}

/* STYLES */
const styles: any = {
  page: {
    display: "flex",
    height: "100vh",
    fontFamily: "Arial",
    background: "linear-gradient(135deg,#eef2ff,#f8fafc)",
  },

  sidebar: {
    width: "300px",
    padding: "20px",
    background: "white",
    borderRight: "1px solid #eee",
    display: "flex",
    flexDirection: "column",
    gap: "10px",
  },

  logo: { color: "#0A66C2" },

  input: {
    padding: "10px",
    border: "1px solid #ccc",
    borderRadius: "8px",
  },

  button: {
    padding: "10px",
    background: "#0A66C2",
    color: "white",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
  },

  main: { flex: 1, padding: "20px", overflowY: "auto" },

  empty: { textAlign: "center", marginTop: "120px" },

  loading: { textAlign: "center", marginTop: "120px" },

  spinner: {
    width: "40px",
    height: "40px",
    border: "4px solid #ddd",
    borderTop: "4px solid #0A66C2",
    borderRadius: "50%",
    margin: "auto",
    animation: "spin 1s linear infinite",
  },

  cards: { display: "flex", gap: "10px", marginBottom: "20px" },

  card: {
    flex: 1,
    background: "white",
    padding: "15px",
    borderRadius: "10px",
  },

  grid: { display: "flex", gap: "20px" },

  panel: { flex: 1, background: "white", padding: "15px", borderRadius: "10px" },

  ai: {
    flex: 1,
    background: "#0A66C2",
    color: "white",
    padding: "15px",
    borderRadius: "10px",
  },

  aiText: {
    whiteSpace: "pre-wrap",
    fontSize: "14px",
    lineHeight: "1.6",
  },

  item: {
    padding: "6px 0",
    borderBottom: "1px solid #eee",
  },
};

/* ANIMATION */
if (typeof window !== "undefined") {
  const style = document.createElement("style");
  style.innerHTML = `
    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
  `;
  document.head.appendChild(style);
}
