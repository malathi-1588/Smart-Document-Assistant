import { useState, useEffect } from "react";

export default function DocumentPreview({ selectedFile }) {
  const [fileData, setFileData] = useState(null);

  useEffect(() => {
    if (selectedFile) {
      fetch(`http://localhost:5000/preview/${selectedFile}`)
        .then((res) => res.json())
        .then((data) => setFileData(data))
        .catch(() => setFileData(null));
    }
  }, [selectedFile]);

  if (!selectedFile) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-center">
        <h2 className="mt-4 text-lg font-semibold">Document Preview</h2>
        <p className="text-gray-500 text-sm">Select a document to preview</p>
      </div>
    );
  }

  if (!fileData) return <p>Loading preview...</p>;

  return (
    <div className="flex flex-col h-full">
      <h2 className="text-lg font-semibold text-center">Preview: {selectedFile}</h2>
      <div className="mt-4 w-full h-96 border rounded-lg overflow-hidden">
        {fileData.type === "pdf" ? (
          <iframe src={fileData.url} className="w-full h-full" title="PDF Preview"></iframe>
        ) : fileData.type === "image" ? (
          <img src={fileData.url} alt="Preview" className="max-h-96 mx-auto" />
        ) : fileData.type === "text" ? (
          <pre className="whitespace-pre-wrap text-sm text-gray-800 p-2 overflow-auto h-full">
            {fileData.content}
          </pre>
        ) : (
          <a
            href={fileData.url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 underline"
          >
            Open Document
          </a>
        )}
      </div>
    </div>
  );
}
