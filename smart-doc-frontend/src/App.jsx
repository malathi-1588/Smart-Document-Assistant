import DocumentUpload from "./components/DocumentUpload";
import DocumentPreview from "./components/DocumentPreview";
import DocumentFetch from "./components/DocumentFetch";

export default function App() {
  return (
    <div className="min-h-screen min-w-screen bg-gray-100 p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Smart Document Assistant
        </h1>
        <p className="text-gray-600 mb-10">
          Upload documents or fetch them by name to access content and insights
        </p>

        {/* Upload + Preview Section */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="bg-white rounded-xl shadow p-6">
            <DocumentUpload />
          </div>
          <div className="bg-white rounded-xl shadow p-6">
            <DocumentPreview />
          </div>
        </div>

        {/* Fetch Section */}
        <div className="mt-8 bg-white rounded-xl shadow p-6">
          <DocumentFetch />
        </div>
      </div>
    </div>
  );
}


