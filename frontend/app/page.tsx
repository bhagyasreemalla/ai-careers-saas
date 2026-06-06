"use client";

import { useState } from "react";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
} from "recharts";

import {
  Target,
  Briefcase,
  Building2,
  TrendingUp,
} from "lucide-react";

export default function Home() {
  const [skills, setSkills] = useState("");
  const [role, setRole] = useState("");
  const [country, setCountry] = useState("");
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const API_URL =
    process.env.NEXT_PUBLIC_API_URL ||
    "http://localhost:8000";

  const analyze = async () => {
    setLoading(true);

    try {
      const res = await fetch(`${API_URL}/analyze`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          skills,
          role,
          country,
          user_id: "demo-user",
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
      <div style={styles.sidebar}>
        <h2 style={styles.logo}>
          AI Career Navigator
        </h2>

        <input
          style={styles.input}
          placeholder="Skills (python, sql)"
          value={skills}
          onChange={(e) => setSkills(e.target.value)}
        />

        <input
          style={styles.input}
          placeholder="Role"
          value={role}
          onChange={(e) => setRole(e.target.value)}
        />

        <input
          style={styles.input}
          placeholder="Country (us, uk, in)"
          value={country}
          onChange={(e) => setCountry(e.target.value)}
        />

        <button
          style={styles.button}
          onClick={analyze}
        >
          {loading
            ? "Analyzing..."
            : "Run Analysis"}
        </button>
      </div>

      <div style={styles.main}>
        {!data && (
          <div style={styles.hero}>
            <h1>🚀 AI Global Career Navigator</h1>
            <p>
              Analyze worldwide demand for your
              skills and get AI-powered career
              recommendations.
            </p>
          </div>
        )}

        {data && (
          <>
            <div style={styles.cards}>
              <MetricCard
                icon={<Target />}
                title="Career Score"
                value={`${data.market_data.market_score}`}
              />

              <MetricCard
                icon={<TrendingUp />}
                title="Hiring Chance"
                value={`${data.market_data.hiring_probability || 80}%`}
              />

              <MetricCard
                icon={<Briefcase />}
                title="Jobs Found"
                value={data.market_data.total_jobs_found}
              />

              <MetricCard
                icon={<Building2 />}
                title="Companies"
                value={
                  data.market_data.top_companies
                    .length
                }
              />
            </div>

            <div style={styles.chartPanel}>
              <h3>📈 Skill Demand Analysis</h3>

              <ResponsiveContainer
                width="100%"
                height={300}
              >
                <BarChart
                  data={data.skill_breakdown}
                >
                  <XAxis dataKey="skill" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="job_count" />
                </BarChart>
              </ResponsiveContainer>
            </div>

            <div style={styles.grid}>
              <div style={styles.panel}>
                <h3>🏢 Top Companies</h3>

                {data.market_data.top_companies.map(
                  (c: string, i: number) => (
                    <div
                      key={i}
                      style={styles.tag}
                    >
                      {c}
                    </div>
                  )
                )}

                <h3
                  style={{
                    marginTop: 20,
                  }}
                >
                  📍 Locations
                </h3>

                {data.market_data.top_locations.map(
                  (l: string, i: number) => (
                    <div
                      key={i}
                      style={styles.tag}
                    >
                      {l}
                    </div>
                  )
                )}

                <h3
                  style={{
                    marginTop: 20,
                  }}
                >
                  💼 Job Titles
                </h3>

                {data.market_data.top_job_titles.map(
                  (t: string, i: number) => (
                    <div
                      key={i}
                      style={styles.tag}
                    >
                      {t}
                    </div>
                  )
                )}
              </div>

              <div style={styles.aiPanel}>
                <h2>
                  🤖 AI Career Copilot
                </h2>

                <div style={styles.aiText}>
                  {data.ai_insight}
                </div>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

function MetricCard({
  title,
  value,
  icon,
}: any) {
  return (
    <div style={styles.card}>
      <div
        style={{
          display: "flex",
          justifyContent:
            "space-between",
        }}
      >
        {icon}
      </div>

      <h4>{title}</h4>

      <h2>{value}</h2>
    </div>
  );
}

const styles: any = {
  page: {
    display: "flex",
    minHeight: "100vh",
    background: "#f4f7fb",
    fontFamily: "Arial",
  },

  sidebar: {
    width: 300,
    background: "white",
    padding: 20,
    borderRight:
      "1px solid #e5e7eb",
    display: "flex",
    flexDirection: "column",
    gap: 12,
  },

  logo: {
    color: "#0A66C2",
  },

  input: {
    padding: 12,
    borderRadius: 8,
    border: "1px solid #ddd",
  },

  button: {
    padding: 12,
    background: "#0A66C2",
    color: "white",
    border: "none",
    borderRadius: 8,
    cursor: "pointer",
  },

  main: {
    flex: 1,
    padding: 24,
  },

  hero: {
    textAlign: "center",
    marginTop: 120,
  },

  cards: {
    display: "grid",
    gridTemplateColumns:
      "repeat(4,1fr)",
    gap: 15,
    marginBottom: 20,
  },

  card: {
    background: "white",
    padding: 20,
    borderRadius: 14,
    boxShadow:
      "0 2px 8px rgba(0,0,0,.05)",
  },

  chartPanel: {
    background: "white",
    padding: 20,
    borderRadius: 14,
    marginBottom: 20,
  },

  grid: {
    display: "grid",
    gridTemplateColumns:
      "1fr 1fr",
    gap: 20,
  },

  panel: {
    background: "white",
    padding: 20,
    borderRadius: 14,
  },

  aiPanel: {
    background: "#0f172a",
    color: "white",
    padding: 24,
    borderRadius: 14,
  },

  aiText: {
    whiteSpace: "pre-wrap",
    lineHeight: 1.7,
  },

  tag: {
    background: "#eef4ff",
    padding: 10,
    borderRadius: 8,
    marginBottom: 8,
  },
};
