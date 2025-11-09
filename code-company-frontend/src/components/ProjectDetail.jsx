import React from "react";
import ReactMarkdown from "react-markdown";

export default function ProjectDetail({ project, onClose }) {
  if (!project) return null;
  const content = project.details_markdown || project.summary || "No details available.";

  return (
    <div className="p-4 border rounded bg-white">
      <div className="flex justify-between items-start">
        <h2 className="text-xl font-bold">{project.title}</h2>
        <button onClick={onClose} className="text-sm text-gray-600">Close</button>
      </div>
      <div className="mt-3 text-sm">
        <ReactMarkdown>{content}</ReactMarkdown>
      </div>
      {project.final_code && (
        <div className="mt-4">
          <h4 className="font-semibold">Code</h4>
          <pre className="bg-gray-100 p-2 rounded"><code>{project.final_code || project.details_markdown}</code></pre>
        </div>
      )}
    </div>
  );
}
