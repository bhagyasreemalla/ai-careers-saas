"use client";

import { useState } from "react";

export default function Home() {
  const [skills, setSkills] = useState("");
  const [role, setRole] = useState("");
  const [country, setCountry] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const analyzeCareer = async () => {
    setLoading(true);

    try {
      const res = await fetch(
        "https://ai-careers-saas.onrender.com/analyze",
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

      const data = await res.json();
      setResult(data);
    } catch (error) {
      console.error(error);
      alert("Error connecting to backend");
    }

    setLoading(false);
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-indigo-950 via-slate-900 to-black text-white p-8">
      <div className="max-w-5xl mx-auto">

        <h1 className="text-5xl font-bold text-center mb-4">
          🚀 AI Global Career Navigator
        </h1>

        <p className="text-center text-gray-300 mb-10">
          Discover your career potential worldwide using AI
        </p>

        <div className="bg-white/10 backdrop-blur-lg rounded-3xl p-8 border border-white/10">

          <input
            className="w-full p-4 rounded-xl text-black mb-4"
            placeholder="Skills (Python, SQL, HR Analytics)"
            value={skills}
            onChange={(e) => setSkills(e.target.value)}
          />

          <input
            className="w-full p-4 rounded-xl text-black mb-4"
            placeholder="Target Role"
            value={role}
            onChange={(e) => setRole(e.target.value)}
          />

          <input
            className="w-full p-4 rounded-xl text-black mb-6"
            placeholder="Country"
            value={country}
            onChange={(e) => setCountry(e.target.value)}
          />

          <button
            onClick={analyzeCareer}
            className="w-full bg-purple-600 hover:bg-purple-700 p-4 rounded-xl font-bold text-lg"
          >
            {loading ? "Analyzing..." : "Analyze Career"}
          </button>
        </div>

        {result && (
          <div className="mt-10 bg-white/10 backdrop-blur-lg rounded-3xl p-8 border border-white/10">
            <h2 className="text-3xl font-bold mb-4">
              Career Insights
            </h2>

            <pre className="overflow-auto whitespace-pre-wrap">
              {JSON.stringify(result, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </main>
  );
}