"use client";

export default function Home() {
  return (
    <main style={{ padding: 40 }}>
      <h1>🚀 AI Career Navigator</h1>

      <p>
        Real-time career intelligence powered by AI and live job market data.
      </p>

      <div style={{ marginTop: 20 }}>
        <input
          placeholder="Skills"
          style={{ padding: 10, marginRight: 10 }}
        />

        <input
          placeholder="Target Role"
          style={{ padding: 10, marginRight: 10 }}
        />

        <input
          placeholder="Country"
          style={{ padding: 10 }}
        />
      </div>

      <button
        style={{
          marginTop: 20,
          padding: "10px 20px",
          cursor: "pointer"
        }}
      >
        Analyze Career Market
      </button>
    </main>
  );
}
