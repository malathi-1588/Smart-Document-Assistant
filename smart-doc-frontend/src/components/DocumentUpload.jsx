import { useState } from "react";
import { CloudArrowUpIcon } from "@heroicons/react/24/outline";

export default function DocumentUpload() {
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  return (
    <div className="text-center">
      <CloudArrowUpIcon style={{ width: "48px", height: "48px" }} className="text-blue-500 mx-auto" />
      <h2 className="mt-4 text-lg font-semibold">Upload Document</h2>
      <p className="text-sm text-gray-500">
        Supports PDF, Word, and image files
      </p>
      <label className="mt-4 inline-block bg-blue-600 text-white px-4 py-2 rounded-lg cursor-pointer hover:bg-blue-700">
        Choose File
        <input type="file" className="hidden" onChange={(e) => setFile(e.target.files[0])} />
      </label>
      {file && (
        <p className="mt-2 text-sm text-gray-700">Selected: {file.name}</p>
      )}
    </div>
  );
}
