import React, { useState } from "react";

export default function RunCompanyButton({ onDone }) {
  const [loading, setLoading] = useState(false);

  const runCompany = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:5000/company/run");
      const json = await res.json();
      console.log("company run:", json);
      if (onDone) onDone(json);
      alert("Company run completed. Check Projects list for new entry.");
    } catch (err) {
      console.error(err);
      alert("Company run failed. See console and backend logs.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <button
      onClick={runCompany}
      disabled={loading}
      className="px-4 py-2 rounded bg-blue-600 text-white"
    >
      {loading ? "Running..." : "Run Company 🚀"}
    </button>
  );
}
