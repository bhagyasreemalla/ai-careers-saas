"use client";

import { useEffect, useState } from "react";

export default function Dashboard() {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    fetch("http://localhost:8000/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        skills: ["Python", "SQL"],
        experience_years: 2,
        target_role: "People Analytics"
      })
    })
      .then(res => res.json())
      .then(setData);
  }, []);

  if (!data) return <div>Loading...</div>;

  return (
    <div style={{ padding: 20 }}>

      <h1>ATS Score: {data.ats_score}</h1>

      <h2>Jobs</h2>
      {data.jobs.map((job: any, i: number) => (
        <div key={i}>
          <b>{job.title}</b> - {job.score}%
        </div>
      ))}

      <h2>AI Insights</h2>
      <pre>{data.insights}</pre>

    </div>
  );
}
