import { useEffect, useState } from "react";

export default function DocumentText({ selectedFile }) {
  const [text, setText] = useState("");
  const [source, setSource] = useState("");

  useEffect(() => {
    if (selectedFile) {
      fetch(`http://localhost:5000/extract/${selectedFile}`)
        .then((res) => res.json())
        .then((data) => {
          setText(data.text || "");
          setSource(data.source || "");
        })
        .catch(() => {
          setText("⚠️ Error extracting text");
          setSource("");
        });
    }
  }, [selectedFile]);

  return (
    <div className="mt-8 bg-white rounded-xl shadow p-6">
      <h2 className="text-lg font-semibold mb-4">Extracted Text</h2>
      {source && (
        <p className="text-xs text-gray-500 mb-2">
          Source: <span className="font-medium">{source}</span>
        </p>
      )}
      <div className="max-h-64 overflow-auto border p-2 rounded text-sm text-gray-800 whitespace-pre-wrap">
        {text ? text : "⚠️ No text extracted"}
      </div>
    </div>
  );
}
