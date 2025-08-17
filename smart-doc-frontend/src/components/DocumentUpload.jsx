import { useState } from "react";
import { CloudArrowUpIcon } from "@heroicons/react/24/outline";

export default function DocumentUpload() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState(""); // success or error message

  const handleFileChange = async (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const res = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();

      if (res.ok) {
        setStatus(`✅ ${data.message}`);
      } else {
        setStatus(`❌ ${data.error || "Upload failed"}`);
      }
    } catch (err) {
      setStatus("❌ Error uploading file");
    }
  };

  return (
    <div className="text-center">
      <CloudArrowUpIcon
        className="w-12 h-12 text-blue-500 mx-auto"
      />
      <h2 className="mt-4 text-lg font-semibold">Upload Document</h2>
      <p className="text-sm text-gray-500">Supports PDF, Word, and image files</p>

      <label className="mt-4 inline-block bg-blue-600 text-white px-4 py-2 rounded-lg cursor-pointer hover:bg-blue-700">
        Choose File
        <input type="file" className="hidden" onChange={handleFileChange} />
      </label>

      {file && (
        <p className="mt-2 text-sm text-gray-700">Selected: {file.name}</p>
      )}

      {status && (
        <p className="mt-2 text-sm font-medium text-green-600">{status}</p>
      )}
    </div>
  );
}
