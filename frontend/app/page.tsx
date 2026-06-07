"use client";

import { useState } from "react";
import ReactECharts from "echarts-for-react";

export default function Page() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const runAnalysis = async () => {
    setLoading(true);

    const res = await fetch("https://YOUR-RENDER-URL.onrender.com/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        skills: ["Python", "SQL", "Excel"],
        experience_years: 2,
        target_role: "People Analytics",
      }),
    });

    const json = await res.json();
    setData(json);
    setLoading(false);
  };

  // ATS GAUGE
  const gaugeOption = {
    series: [
      {
        type: "gauge",
        progress: { show: true },
        detail: { valueAnimation: true, formatter: "{value}%" },
        data: [{ value: data?.ats_score || 0 }],
      },
    ],
  };

  // JOB CHART
  const jobOption = {
    xAxis: {
      type: "category",
      data: data?.job_matches?.map((j: any) => j.title) || [],
    },
    yAxis: { type: "value" },
    series: [
      {
        data: data?.job_matches?.map((j: any) => j.match_score) || [],
        type: "bar",
      },
    ],
  };

  return (
    <div style={{ padding: 30, fontFamily: "Arial" }}>
      <h1>🚀 AI Career Copilot V5</h1>

      <button onClick={runAnalysis}>
        {loading ? "Analyzing..." : "Run AI Analysis"}
      </button>

      {data && (
        <>
          <h2>ATS Score</h2>
          <ReactECharts option={gaugeOption} />

          <h2>Job Matches</h2>
          <ReactECharts option={jobOption} />

          <h2>Missing Skills</h2>
          <pre>{JSON.stringify(data.missing_skills, null, 2)}</pre>

          <h2>AI Insight</h2>
          <p>{data.ai_insight}</p>

          <h2>Job Links</h2>
          {data.job_matches.map((job: any, i: number) => (
            <div key={i}>
              <a href={job.link} target="_blank">
                {job.title} ({job.match_score}% match)
              </a>
            </div>
          ))}
        </>
      )}
    </div>
  );
}
