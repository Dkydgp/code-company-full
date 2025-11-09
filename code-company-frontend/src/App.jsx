import { useEffect, useState } from "react";
import Modal from "react-modal";
import { motion } from "framer-motion";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";

Modal.setAppElement("#root");

function App() {
  const [message, setMessage] = useState("Connecting...");
  const [projects, setProjects] = useState([]);
  const [selected, setSelected] = useState(null);
  const [loading, setLoading] = useState(false);

  // ✅ Helper function to handle multiple code key formats from backend
  const getProjectCode = (p) => {
    return (
      p.final_code ||
      p.details?.operations?.final_code ||
      p.details?.ceo?.final_code ||
      p.details_markdown ||
      "# No code available."
    );
  };

  // 🔌 Backend connection check
  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/test")
      .then((res) => res.json())
      .then((data) => setMessage(data.message))
      .catch(() => setMessage("⚠️ Backend not reachable"));
  }, []);

  // 📦 Load all projects
  const loadProjects = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:5000/api/projects");
      const json = await res.json();
      setProjects(json.projects || []);
    } catch {
      alert("❌ Failed to fetch projects");
    } finally {
      setLoading(false);
    }
  };

  // 🧠 Run AI Company pipeline
  const runCompany = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:5000/company/run");
      const data = await res.json();
      alert("✅ New project completed by AI Company!");
      loadProjects();
    } catch {
      alert("❌ Company run failed");
    } finally {
      setLoading(false);
    }
  };

  // 💾 Code download
  const downloadCode = (project) => {
    const code = getProjectCode(project);
    if (!code || code === "# No code available.") return alert("No code available to download!");
    const blob = new Blob([code], { type: "text/x-python" });
    const link = document.createElement("a");
    const safeName = (project.title || "code_project").replace(/[^a-z0-9]/gi, "_").toLowerCase();
    link.href = URL.createObjectURL(blob);
    link.download = `${safeName}.py`;
    link.click();
  };

  const latestProject = projects[projects.length - 1];

  return (
    <div className="min-h-screen flex bg-gradient-to-br from-blue-100 via-white to-blue-50 text-gray-800">
      {/* Sidebar */}
      <aside className="w-64 hidden md:flex flex-col justify-between p-6 bg-white/70 backdrop-blur-lg shadow-lg">
        <div>
          <h1 className="text-2xl font-bold text-blue-600 mb-8">Code Company ⚙️</h1>
          <nav className="flex flex-col space-y-4">
            <button onClick={loadProjects} className="text-left text-gray-700 hover:text-blue-600 transition">
              📁 Projects
            </button>
            <button onClick={runCompany} className="text-left text-gray-700 hover:text-green-600 transition">
              🤖 Run Company
            </button>
            <a href="#" className="text-left text-gray-700 hover:text-purple-600 transition">👥 Team</a>
            <a href="#" className="text-left text-gray-700 hover:text-indigo-600 transition">📨 Contact</a>
          </nav>
        </div>
        <div className="text-sm text-gray-500">© {new Date().getFullYear()} Code Company</div>
      </aside>

      {/* Main Dashboard */}
      <main className="flex-1 flex flex-col items-center py-10 px-6">
        <motion.h2
          className="text-4xl md:text-5xl font-extrabold text-blue-700 mb-2"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          Welcome to <span className="text-blue-500">Code Company</span>
        </motion.h2>

        <p className="text-gray-600 mb-8 text-center max-w-2xl">
          Automating intelligent project creation — from idea to code execution.
        </p>

        {/* Buttons */}
        <div className="flex flex-wrap justify-center gap-4 mb-8">
          <motion.button
            onClick={loadProjects}
            disabled={loading}
            whileHover={{ scale: 1.05 }}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg font-semibold shadow hover:bg-blue-700 transition"
          >
            {loading ? "Loading..." : "Explore Projects 🚀"}
          </motion.button>
          <motion.button
            onClick={runCompany}
            disabled={loading}
            whileHover={{ scale: 1.05 }}
            className="px-6 py-3 bg-green-600 text-white rounded-lg font-semibold shadow hover:bg-green-700 transition"
          >
            {loading ? "Running..." : "Run Company 🤖"}
          </motion.button>
        </div>

        {/* Backend Status */}
        <div className="text-gray-700 bg-white/70 backdrop-blur-md px-4 py-2 rounded-md shadow-sm mb-10">
          <span className="font-medium">Backend Status:</span> {message}
        </div>

        {/* Latest Project */}
        {latestProject && (
          <motion.div
            className="w-full max-w-4xl bg-white/80 rounded-2xl shadow-lg p-6 mb-10 border border-blue-100"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <h3 className="text-2xl font-bold text-blue-700 mb-2">🚀 Latest Project</h3>
            <h4 className="text-lg font-semibold mb-2">{latestProject.title}</h4>
            <p className="text-gray-700 mb-4">{latestProject.summary || "No summary provided."}</p>
            <div className="flex justify-between items-center">
              <span
                className={`px-3 py-1 text-sm font-medium rounded-full ${
                  latestProject.status === "success"
                    ? "bg-green-100 text-green-700"
                    : "bg-red-100 text-red-700"
                }`}
              >
                {latestProject.status}
              </span>
              <button
                onClick={() => setSelected(latestProject)}
                className="text-sm text-blue-600 underline hover:text-blue-800"
              >
                View Details
              </button>
            </div>
          </motion.div>
        )}

        {/* Dropdown for all project codes */}
        {projects.length > 0 && (
          <div className="w-full max-w-5xl mb-10">
            <h3 className="text-2xl font-semibold text-gray-800 mb-4">🧠 All Project Codes</h3>
            <details className="bg-white/80 rounded-lg shadow border border-blue-100">
              <summary className="cursor-pointer px-4 py-3 font-medium text-blue-700">
                Show All Project Codes ▼
              </summary>
              <div className="p-4 space-y-6">
                {projects.map((p, i) => (
                  <div key={i} className="border-b border-gray-200 pb-4">
                    <h4 className="font-semibold text-blue-700 mb-2">{p.title}</h4>
                    <SyntaxHighlighter language="python" style={oneDark} wrapLongLines={true}>
                      {getProjectCode(p)}
                    </SyntaxHighlighter>
                  </div>
                ))}
              </div>
            </details>
          </div>
        )}

        {/* Projects Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 w-full max-w-6xl">
          {projects.map((p, i) => (
            <motion.div
              key={i}
              className="p-6 bg-white/70 backdrop-blur-md rounded-2xl shadow hover:shadow-xl transition border border-blue-100"
              whileHover={{ scale: 1.03 }}
            >
              <h3 className="text-xl font-semibold text-blue-700 mb-2">{p.title}</h3>
              <p className="text-gray-600 mb-4 line-clamp-4">{p.summary || "No summary available."}</p>
              <div className="flex items-center justify-between">
                <span
                  className={`px-3 py-1 text-sm font-medium rounded-full ${
                    p.status === "success"
                      ? "bg-green-100 text-green-700"
                      : "bg-red-100 text-red-700"
                  }`}
                >
                  {p.status}
                </span>
                <button
                  onClick={() => setSelected(p)}
                  className="text-sm text-blue-600 underline hover:text-blue-800"
                >
                  View Details
                </button>
              </div>
            </motion.div>
          ))}
        </div>
      </main>

      {/* Modal for Project Details */}
      <Modal
        isOpen={!!selected}
        onRequestClose={() => setSelected(null)}
        contentLabel="Project Details"
        className="max-w-4xl mx-auto mt-20 bg-white p-6 rounded-lg shadow-xl outline-none"
        overlayClassName="fixed inset-0 bg-black/50 flex justify-center items-start overflow-auto"
      >
        {selected && (
          <motion.div
            initial={{ opacity: 0, y: -30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
          >
            <h2 className="text-2xl font-bold text-blue-700 mb-4">{selected.title}</h2>
            <h3 className="text-lg font-semibold mb-2">Summary</h3>
            <p className="mb-4 text-gray-700 whitespace-pre-line">
              {selected.solution_summary || selected.summary || "No summary provided."}
            </p>

            <h3 className="text-lg font-semibold mb-2">Code</h3>
            <SyntaxHighlighter language="python" style={oneDark} wrapLongLines={true}>
              {getProjectCode(selected)}
            </SyntaxHighlighter>

            <button
              onClick={() => downloadCode(selected)}
              className="px-3 py-2 bg-green-600 text-white rounded hover:bg-green-700 my-4"
            >
              💾 Download Code (.py)
            </button>

            <h3 className="text-lg font-semibold mb-2">Conclusion</h3>
            <p className="text-gray-700 whitespace-pre-line">
              {selected.conclusion || "No conclusion available."}
            </p>

            <button
              onClick={() => setSelected(null)}
              className="mt-6 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              Close
            </button>
          </motion.div>
        )}
      </Modal>
    </div>
  );
}

export default App;
