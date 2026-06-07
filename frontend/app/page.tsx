"use client";

import { useState } from "react";
import ReactECharts from "echarts-for-react";

export default function Page() {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<any>(null);

  const analyze = async () => {
    try {
      setLoading(true);

      const res = await fetch(
        "https://ai-careers-saas.onrender.com/analyze",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            skills: ["Python", "SQL"],
            experience_years: 2,
            target_role: "People Analytics",
          }),
        }
      );

      const json = await res.json();
      setData(json);
    } catch (err) {
      console.error("API Error:", err);
    } finally {
      setLoading(false);
    }
  };

  const gaugeOption = (score: number) => ({
    series: [
      {
        type: "gauge",
        progress: { show: true },
        detail: { valueAnimation: true, formatter: "{value}%" },
        data: [{ value: score }],
      },
    ],
  });

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>🚀 AI Career Copilot V5</h1>

      <button onClick={analyze} style={styles.button}>
        {loading ? "Analyzing..." : "Run AI Analysis"}
      </button>

      {!data && !loading && (
        <p style={{ marginTop: 20 }}>Click analyze to generate insights</p>
      )}

      {data && (
        <div style={styles.grid}>
          {/* ATS SCORE */}
          <div style={styles.card}>
            <h2>ATS Score</h2>
            <ReactECharts
              option={gaugeOption(data.ats_score)}
              style={{ height: 250 }}
            />
          </div>

          {/* MISSING SKILLS */}
          <div style={styles.card}>
            <h2>Missing Skills</h2>
            <ul>
              {data.missing_skills.map((skill: string, i: number) => (
                <li key={i}>⚠ {skill}</li>
              ))}
            </ul>
          </div>

          {/* JOB MATCHES */}
          <div style={styles.card}>
            <h2>Top Jobs</h2>
            {data.job_matches.map((job: any, i: number) => (
              <div key={i} style={styles.jobCard}>
                <h3>{job.title}</h3>
                <p>Match: {job.score}%</p>
                <a href={job.link} target="_blank">
                  View Job →
                </a>
              </div>
            ))}
          </div>

          {/* AI INSIGHT */}
          <div style={{ ...styles.card, gridColumn: "span 2" }}>
            <h2>AI Career Insight</h2>
            <pre style={{ whiteSpace: "pre-wrap" }}>
              {data.ai_insight}
            </pre>
          </div>
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
    color: "white",
    minHeight: "100vh",
  },
  title: {
    fontSize: 28,
    marginBottom: 20,
  },
  button: {
    padding: "10px 20px",
    background: "#38bdf8",
    border: "none",
    borderRadius: 8,
    cursor: "pointer",
    fontWeight: "bold",
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(2, 1fr)",
    gap: 20,
    marginTop: 30,
  },
  card: {
    background: "#1e293b",
    padding: 20,
    borderRadius: 12,
  },
  jobCard: {
    padding: 10,
    marginBottom: 10,
    background: "#0f172a",
    borderRadius: 8,
  },
};
