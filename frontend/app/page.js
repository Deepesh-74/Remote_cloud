"use client";

import { useState } from "react";
import "./styles.css";

const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function Home() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function analyze(event) {
    event.preventDefault();
    if (!file) {
      setError("Choose an image first.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);
    const form = new FormData();
    form.append("file", file);

    try {
      const response = await fetch(`${apiUrl}/report`, { method: "POST", body: form });
      const body = await response.json();
      if (!response.ok) throw new Error(body.detail || "Analysis failed.");
      setResult(body);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main>
      <section>
        <p className="eyebrow">AI Media Forensics</p>
        <h1>Inspect an image with an explainable baseline.</h1>
        <p className="intro">Upload an image to review metadata and simple visual-consistency indicators.</p>
        <form onSubmit={analyze}>
          <input type="file" accept="image/*" onChange={(event) => setFile(event.target.files?.[0] || null)} />
          <button disabled={loading}>{loading ? "Analyzing..." : "Analyze image"}</button>
        </form>
        {error && <p className="error">{error}</p>}
      </section>
      {result && (
        <section className="result">
          <h2>{result.prediction.label.replace("_", " ")}</h2>
          <p>Confidence: {Math.round(result.prediction.confidence * 100)}%</p>
          <pre>{JSON.stringify(result.forensic_indicators, null, 2)}</pre>
          <p className="note">{result.limitations[0]}</p>
        </section>
      )}
    </main>
  );
}
