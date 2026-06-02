"use client";

import { useState } from "react";

export default function Home() {
  const [skills, setSkills] = useState("");
  const [role, setRole] = useState("");
  const [country, setCountry] = useState("");

  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState("");

  const analyze = async () => {
    setLoading(true);
    setError("");
    setData(null);

    try {
      const res = await fetch("https://YOUR_BACKEND_URL.onrender.com/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ skills, role, country }),
      });

      const result = await res.json();

      if (!res.ok) throw new Error(result.detail || "API Error");

      setData(result);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-950 text-white p-6">
      <div className="max-w-5xl mx-auto">

        {/* HEADER */}
        <h1 className="text-3xl font-bold mb-2">
          AI Career Navigator 🚀
        </h1>
        <p className="text-gray-400 mb-8">
          Analyze your global career potential instantly
        </p>

        {/* INPUT BOX */}
        <div className="bg-gray-900 p-6 rounded-xl shadow-lg mb-8">
          <div className="grid gap-4 md:grid-cols-3">
            
            <input
              className="p-3 rounded bg-gray-800 text-white"
              placeholder="Skills (e.g. HR, Jira)"
              value={skills}
              onChange={(e) => setSkills(e.target.value)}
            />

            <input
              className="p-3 rounded bg-gray-800 text-white"
              placeholder="Target Role"
              value={role}
              onChange={(e) => setRole(e.target.value)}
            />

            <input
              className="p-3 rounded bg-gray-800 text-white"
              placeholder="Country"
              value={country}
              onChange={(e) => setCountry(e.target.value)}
            />
          </div>

          <button
            onClick={analyze}
            className="mt-4 bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded font-semibold"
          >
            {loading ? "Analyzing..." : "Analyze Career"}
          </button>
        </div>

        {/* ERROR */}
        {error && (
          <div className="bg-red-900 text-red-200 p-4 rounded mb-6">
            {error}
          </div>
        )}

        {/* RESULTS */}
        {data && (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">

            <Card title="Career Score" value={data.career_score} />
            <Card title="Visa Score" value={data.visa_score} />
            <Card title="Competition" value={data.competition} />
            <Card title="Salary Range" value={data.salary_range} />

            <div className="bg-gray-900 p-4 rounded-xl col-span-full">
              <h3 className="font-bold mb-2">Missing Skills</h3>
              <div className="flex flex-wrap gap-2">
                {data.missing_skills?.map((s: string, i: number) => (
                  <span key={i} className="bg-gray-800 px-3 py-1 rounded-full text-sm">
                    {s}
                  </span>
                ))}
              </div>
            </div>

            <div className="bg-gray-900 p-4 rounded-xl">
              <h3 className="font-bold mb-2">Top Countries</h3>
              <ul className="text-gray-300 space-y-1">
                {data.top_countries?.map((c: string, i: number) => (
                  <li key={i}>🌍 {c}</li>
                ))}
              </ul>
            </div>

            <div className="bg-gray-900 p-4 rounded-xl col-span-full">
              <h3 className="font-bold mb-2">AI Insight</h3>
              <p className="text-gray-300 whitespace-pre-line">
                {data.ai_insight}
              </p>
            </div>

            <div className="bg-gray-900 p-4 rounded-xl col-span-full">
              <h3 className="font-bold mb-2">Roadmap</h3>
              <ol className="list-decimal ml-5 text-gray-300">
                {data.roadmap?.map((r: string, i: number) => (
                  <li key={i}>{r}</li>
                ))}
              </ol>
            </div>

          </div>
        )}
      </div>
    </div>
  );
}

/* CARD COMPONENT */
function Card({ title, value }: any) {
  return (
    <div className="bg-gray-900 p-6 rounded-xl shadow">
      <h3 className="text-gray-400 text-sm">{title}</h3>
      <p className="text-2xl font-bold mt-2">{value}</p>
    </div>
  );
}