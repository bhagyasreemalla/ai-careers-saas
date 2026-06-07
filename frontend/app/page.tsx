"use client";

import { useState } from "react";
import ReactECharts from "echarts-for-react";

export default function Page() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [data, setData] = useState<any>(null);

  const analyze = async () => {
    try {
      setLoading(true);
      setError("");

      const res = await fetch(
        "https://ai-careers-saas.onrender.com/analyze",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            skills: ["Python", "SQL"],
            experience_years: 2,
            target_role: "People Analytics",
          }),
        }
      );

      if (!res.ok) throw new Error("API failed");

      const json = await res.json();
      setData(json);
    } catch (err: any) {
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  const gaugeOption = (value: number) => ({
    series: [
      {
        type: "gauge",
        progress: { show: true, width: 18 },
        axisLine: {
          lineStyle: {
            width: 18,
            color: [
              [0.3, "#ef4444"],
              [0.7, "#f59e0b"],
              [1, "#22c55e"],
            ],
          },
        },
        detail: {
          valueAnimation: true,
          formatter: "{value}%",
          fontSize: 20,
        },
        data: [{ value }],
      },
    ],
  });

  const barOption = (jobs: any[]) => ({
    xAxis: {
      type: "category",
      data: jobs.map((j) => j.title),
      axisLabel: { rotate: 20 },
    },
    yAxis: { type: "value" },
    series: [
      {
        data: jobs.map((j) => j.score),
        type: "bar",
        itemStyle: { borderRadius: 6 },
      },
    ],
  });

  return (
    <div style={styles.page}>
      {/* HEADER */}
      <div style={styles.header}>
        <h1>🚀 AI Career Copilot V5</h1>
        <p>Smart ATS • Job Matching • AI Insights</p>
      </div>

      {/* ACTION */}
      <button onClick={analyze} style={styles.button}>
        {loading ? "Analyzing..." : "Run AI Analysis"}
      </button>

      {error && <p style={styles.error}>{error}</p>}

      {/* EMPTY STATE */}
      {!data && !loading && (
        <div style={styles.empty}>
          <p>Click analyze to generate your career intelligence report</p>
        </div>
      )}

      {/* DASHBOARD */}
      {data && (
        <div style={styles.grid}>
          {/* ATS SCORE */}
          <div style={styles.card}>
            <h2>ATS Score</h2>
            <ReactECharts option={gaugeOption(data.ats_score)} />
          </div>

          {/* SKILLS */}
          <div style={styles.card}>
            <h2>Skill Gap</h2>
            {data.missing_skills?.length ? (
              <ul>
                {data.missing_skills.map((s: string, i: number) => (
                  <li key={i}>⚠ {s}</li>
                ))}
              </ul>
            ) : (
              <p>All core skills matched 🎯</p>
            )}
          </div>

          {/* JOB CHART */}
          <div style={{ ...styles.card, gridColumn: "span 2" }}>
            <h2>Job Match Score</h2>
            <ReactECharts option={barOption(data.job_matches)} />
          </div>

          {/* JOB LIST */}
          <div style={styles.card}>
            <h2>Top Roles</h2>
            {data.job_matches?.map((job: any, i: number) => (
              <div key={i} style={styles.jobCard}>
                <strong>{job.title}</strong>
                <p>{job.score}% match</p>
                <a href={job.link} target="_blank">
                  View →
                </a>
              </div>
            ))}
          </div>

          {/* AI INSIGHT */}
          <div style={{ ...styles.card, gridColumn: "span 2" }}>
            <h2>AI Career Intelligence</h2>
            <pre style={styles.aiBox}>{data.ai_insight}</pre>
          </div>
        </div>
      )}
    </div>
  );
}

/* ---------------- STYLES ---------------- */

const styles: any = {
  page: {
    padding: 30,
    fontFamily: "Arial",
    background: "#0b1220",
    color: "#fff",
    minHeight: "100vh",
  },

  header: {
    marginBottom: 20,
  },

  button: {
    padding: "12px 20px",
    background: "#38bdf8",
    border: "none",
    borderRadius: 10,
    fontWeight: "bold",
    cursor: "pointer",
  },

  error: {
    color: "#f87171",
    marginTop: 10,
  },

  empty: {
    marginTop: 30,
    opacity: 0.7,
  },

  grid: {
    marginTop: 30,
    display: "grid",
    gridTemplateColumns: "repeat(2, 1fr)",
    gap: 20,
  },

  card: {
    background: "#111827",
    padding: 20,
    borderRadius: 14,
    boxShadow: "0 10px 25px rgba(0,0,0,0.3)",
  },

  jobCard: {
    background: "#0f172a",
    padding: 10,
    borderRadius: 10,
    marginBottom: 10,
  },

  aiBox: {
    whiteSpace: "pre-wrap",
    background: "#0f172a",
    padding: 15,
    borderRadius: 10,
  },
};
