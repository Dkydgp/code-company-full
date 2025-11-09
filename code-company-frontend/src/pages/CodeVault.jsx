import { useEffect, useState } from "react";
import ProjectCard from "../components/ProjectCard";

const BACKEND = "http://127.0.0.1:5000";

export default function CodeVault() {
  const [history, setHistory] = useState([]);

  async function loadHistory() {
    try {
      const res = await fetch(`${BACKEND}/company/history`);
      if (!res.ok) throw new Error("fetch failed");
      const data = await res.json();
      setHistory(Array.isArray(data) ? data.reverse() : []);
    } catch (e) {
      console.error(e);
      setHistory([]);
    }
  }

  useEffect(() => {
    loadHistory();
  }, []);

  return (
    <div className="max-w-6xl mx-auto px-4 py-10">
      <h1 className="text-3xl font-bold mb-6">📜 Code Vault</h1>

      {history.length === 0 ? (
        <div className="text-center text-gray-500 p-6 bg-white rounded shadow">
          No history yet. Use Run Company to create projects.
        </div>
      ) : (
        history.map((project, i) => {
          const title = project.details?.technical?.project_title || `Project ${i + 1}`;
          const ceo = project.details?.ceo?.decision || "n/a";
          const summary = project.details?.operations?.solution_summary || project.details?.operations?.conclusion || "";
          const code = project.details?.operations?.final_code || "";
          return (
            <details key={i} className="mb-4 bg-white rounded shadow p-4 border">
              <summary className="cursor-pointer font-semibold text-lg">
                {title} <span className="ml-2 text-sm text-gray-500">({ceo})</span>
              </summary>
              <div className="mt-3 text-gray-700">
                <p className="mb-2">
                  <strong>CEO:</strong> {project.details?.ceo?.reason || project.details?.ceo?.decision}
                </p>
                <p className="mb-3">
                  <strong>Summary:</strong> {summary}
                </p>

                {code && (
                  <div className="mt-2">
                    <ProjectCard code={code} language="python" />
                  </div>
                )}
              </div>
            </details>
          );
        })
      )}
    </div>
  );
}

