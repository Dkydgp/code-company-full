import { useEffect, useState } from "react";
import LatestProject from "../components/LatestProject";

const BACKEND = "http://127.0.0.1:5000";

export default function Home() {
  const [latest, setLatest] = useState(null);
  const [status, setStatus] = useState("Checking backend...");
  const [running, setRunning] = useState(false);

  async function fetchHistory() {
    try {
      const res = await fetch(`${BACKEND}/company/history`);
      if (!res.ok) throw new Error("history fetch failed");
      const data = await res.json();
      if (Array.isArray(data) && data.length > 0) {
        setLatest(data[data.length - 1]);
      } else {
        setLatest(null);
      }
    } catch {
      setLatest(null);
    }
  }

  async function checkBackend() {
    try {
      const res = await fetch(`${BACKEND}/api/test`);
      await res.json();
      setStatus("✅ Connected");
    } catch {
      setStatus("⚠️ Backend offline");
    }
  }

  useEffect(() => {
    checkBackend();
    fetchHistory();
    const id = setInterval(fetchHistory, 10000);
    return () => clearInterval(id);
  }, []);

  async function runCompany() {
    setRunning(true);
    try {
      const res = await fetch(`${BACKEND}/company/run`, { method: "POST" });
      const json = await res.json();
      await fetchHistory();
      alert("✅ Company run completed: " + (json.company || "Done"));
    } catch {
      alert("❌ Failed to run company. Check backend logs.");
    } finally {
      setRunning(false);
    }
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-10">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-4xl font-bold">Welcome to Code Company</h1>
          <p className="text-gray-600 mt-2">
            Automating intelligent project creation — from idea to code execution.
          </p>
        </div>

        <div className="text-right">
          <div className="text-sm text-gray-500 mb-2">
            Backend Status: <span className="font-medium">{status}</span>
          </div>
          <button
            onClick={runCompany}
            disabled={running}
            className={`px-4 py-2 rounded ${
              running ? "bg-gray-400" : "bg-green-600 hover:bg-green-700 text-white"
            }`}
          >
            {running ? "Running..." : "🤖 Run Company"}
          </button>
        </div>
      </div>

      <section className="mb-10">
        <h3 className="text-xl font-semibold mb-3">Latest Project 🚀</h3>
        <LatestProject project={latest} />
      </section>

      <section>
        <h3 className="text-xl font-semibold mb-3">Quick Actions</h3>
        <div className="flex gap-3">
          <button onClick={fetchHistory} className="px-3 py-2 bg-indigo-600 text-white rounded">
            Refresh Latest
          </button>
          <a href="/codes" className="px-3 py-2 border rounded">
            Open Code Vault
          </a>
        </div>
      </section>
    </div>
  );
}
