import { Light as SyntaxHighlighter } from "react-syntax-highlighter";
import python from "react-syntax-highlighter/dist/esm/languages/hljs/python";
import { atomOneDark } from "react-syntax-highlighter/dist/esm/styles/hljs";

SyntaxHighlighter.registerLanguage("python", python);

export default function ProjectCard({ code, language = "python" }) {
  if (!code) return <div className="text-sm text-gray-500">No code available.</div>;

  return (
    <div className="rounded-md overflow-hidden border border-gray-200">
      <div className="bg-gray-900 p-3">
        <SyntaxHighlighter language={language} style={atomOneDark} customStyle={{ margin: 0, background: "transparent" }}>
          {code}
        </SyntaxHighlighter>
      </div>
    </div>
  );
}
