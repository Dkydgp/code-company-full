import { useState } from "react";
import ProjectCard from "./ProjectCard";

export default function LatestProject({ project }) {
  const [expanded, setExpanded] = useState(false);
  if (!project) {
    return (
      <div className="bg-white shadow rounded-lg p-6 text-center">
        <div className="text-gray-500">No latest project yet. Click <strong>Run Company</strong> to create one.</div>
      </div>
    );
  }

  const title = project.details?.technical?.project_title || "Untitled Project";
  const ceoDecision = project.details?.ceo?.decision || "unknown";
  const opSummary = project.details?.operations?.solution_summary || project.details?.operations?.conclusion || "";
  const code = project.details?.operations?.final_code || "";

  return (
    <div className="bg-white shadow-lg rounded-2xl p-6">
      <div className="flex items-start justify-between">
        <div>
          <h2 className="text-2xl font-bold">{title}</h2>
          <div className="mt-2 flex items-center gap-3">
            <span className={`px-2 py-1 text-sm rounded ${ceoDecision === "approve" ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"}`}>
              CEO: {ceoDecision}
            </span>
            <span className="text-xs text-gray-500">Latest</span>
          </div>
        </div>

        <div className="text-right">
          <button
            onClick={() => setExpanded((s) => !s)}
            className="px-3 py-1 bg-indigo-600 text-white rounded hover:bg-indigo-700"
          >
            {expanded ? "Hide Code" : "View Code"}
          </button>
        </div>
      </div>

      <p className="mt-4 text-gray-700">{opSummary}</p>

      {expanded && (
        <div className="mt-4">
          <ProjectCard code={code} language="python" />
        </div>
      )}
    </div>
  );
}
