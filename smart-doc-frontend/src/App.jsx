import { useState } from "react";
import Login from "./components/Login";
import Signup from "./components/Signup";
import DocumentUpload from "./components/DocumentUpload";
import DocumentPreview from "./components/DocumentPreview";
import DocumentFetch from "./components/DocumentFetch";
import DocumentText from "./components/DocumentText";

export default function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [refreshDocs, setRefreshDocs] = useState(false);
  const [username, setUsername] = useState(localStorage.getItem("username"));
  const [token, setToken] = useState(localStorage.getItem("token"));

  const handleFileUploaded = (filename) => {
    setSelectedFile(filename);
    setRefreshDocs((prev) => !prev);
  };

  const handleLogout = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("username");
  setUsername(null);
  setSelectedFile(null); // clear selected file
  window.location.reload(); //refresh page
};


  if (!token) {
    return (
      <div className="min-h-screen min-w-screen flex items-center justify-center bg-gray-200"> 
        <div className="flex gap-6">
          <Login
            onLogin={(res) => {
              localStorage.setItem("token", res.token);
              localStorage.setItem("username", res.username);
              setToken(res.token);
              setUsername(res.username);
            }}
          />
          <Signup />
        </div>
      </div>
    );
  }

  return (
  <div className="min-h-screen min-w-screen bg-gray-100 p-8">
    <div className="max-w-7xl mx-auto px-2">
      {/* Header Section */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Smart Document Assistant</h1>
          <p className="text-gray-600">
            Upload documents or fetch them by name to access content and insights {username}
          </p>
        </div>
        <button
          onClick={handleLogout}
          className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded"
        >
          Logout
        </button>
      </div>

      {/* Main Layout */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
        <div className="flex flex-col gap-8 md:col-span-2">
          <div className="bg-white rounded-xl shadow p-6">
            <DocumentUpload onFileUploaded={handleFileUploaded} />
          </div>
          <div className="bg-white rounded-xl shadow p-6">
            <DocumentFetch onSelectFile={setSelectedFile} refreshTrigger={refreshDocs} />
          </div>
        </div>

        <div className="bg-white rounded-xl shadow p-6 md:col-span-2">
          <DocumentPreview selectedFile={selectedFile} />
        </div>
      </div>

      {/* Extracted Text Section */}
      {selectedFile && (
        <div className="mt-8">
          <DocumentText selectedFile={selectedFile} />
        </div>
      )}
    </div>
  </div>
);

}


        

