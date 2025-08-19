import DocumentUpload from "./components/DocumentUpload";
import DocumentPreview from "./components/DocumentPreview";
import DocumentFetch from "./components/DocumentFetch";
import DocumentText from "./components/DocumentText";
import { useState } from "react";

export default function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [refreshDocs, setRefreshDocs] = useState(false);

  const handleFileUploaded = (filename) => {
    setSelectedFile(filename);
    setRefreshDocs((prev) => !prev);
  };

  return (
    <div className="min-h-screen min-w-screen bg-gray-100 p-8">
      <div className="max-w-7xl mx-auto px-2">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Smart Document Assistant
        </h1>
        <p className="text-gray-600 mb-10">
          Upload documents or fetch them by name to access content and insights
        </p>

        {/* Upload + Fetch + Preview side by side */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Left side: Upload + Fetch */}
          <div className="flex flex-col gap-8 md:col-span-2">
            <div className="bg-white rounded-xl shadow p-6">
              <DocumentUpload onFileUploaded={handleFileUploaded} />
            </div>
            <div className="bg-white rounded-xl shadow p-6">
              <DocumentFetch
                onSelectFile={setSelectedFile}
                refreshTrigger={refreshDocs}
              />
            </div>
          </div>

          {/* Right side: Preview (fixed height) */}
          <div className="bg-white rounded-xl shadow p-6 md:col-span-2 h-[600px]">
            <DocumentPreview selectedFile={selectedFile} />
          </div>
        </div>

        {/* Extracted Text (separate, does not affect preview height) */}
        {selectedFile && (
          <div className="mt-8">
            <DocumentText selectedFile={selectedFile} />
          </div>
        )}
      </div>
    </div>
  );
}
