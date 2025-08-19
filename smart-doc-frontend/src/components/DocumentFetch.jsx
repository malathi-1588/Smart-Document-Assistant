import { MagnifyingGlassIcon, ClockIcon } from "@heroicons/react/24/outline";
import { useState, useEffect } from "react";

export default function DocumentFetch({ onSelectFile }) {
  const [docName, setDocName] = useState("");
  const [recentSearches, setRecentSearches] = useState([]);
  const [results, setResults] = useState([]);
  const [error, setError] = useState("");

  // Load recent docs on page load
  useEffect(() => {
    fetch("http://localhost:5000/documents")
      .then((res) => res.json())
      .then((data) => setRecentSearches(data))
      .catch((err) => console.error("Error fetching documents:", err));
  }, []);

  // Handle search
  const handleSearch = (e) => {
    e.preventDefault(); // stop page reload
    if (!docName.trim()) return;

    fetch(`http://localhost:5000/documents/${docName}`)
      .then((res) => {
        if (!res.ok) throw new Error("No documents found");
        return res.json();
      })
      .then((data) => {
        setResults(data);
        setError("");
      })
      .catch((err) => {
        setResults([]);
        setError(err.message);
      });
  };

  return (
    <div>
      <h2 className="text-lg font-semibold mb-4">Fetch Document</h2>

      {/* Search row */}
      <form onSubmit={handleSearch} className="flex">
        <input
          type="text"
          placeholder="Enter document name..."
          value={docName}
          onChange={(e) => setDocName(e.target.value)}
          className="flex-1 text-black bg-white border border-gray-300 rounded-l-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded-r-lg hover:bg-blue-700 flex items-center justify-center"
        >
          <MagnifyingGlassIcon className="w-5 h-5" />
        </button>
      </form>

      {/* Error message */}
      {error && <p className="text-red-500 mt-2">{error}</p>}

      {/* Search results */}
      {results.length > 0 && (
        <div className="mt-4">
          <h3 className="text-gray-700 font-semibold">Search Results</h3>
          <ul className="mt-2 space-y-1">
            {results.map((doc) => (
              <li
                key={doc.id}
                className="text-blue-600 hover:underline cursor-pointer"
                onClick={() => {
                  setDocName(doc.filename);
                  onSelectFile(doc.filename); // 🔥 update preview
                }}
              >
                {doc.filename}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Recent searches */}
      <div className="mt-6">
        <p className="text-gray-500 flex items-center gap-2">
          <ClockIcon className="w-4 h-4" /> Recent Documents
        </p>
        <ul className="mt-2 space-y-1">
          {recentSearches.map((item) => (
            <li
              key={item.id}
              className="text-blue-600 cursor-pointer hover:underline"
              onClick={() => {
                setDocName(item.filename);
                onSelectFile(item.filename); // 🔥 update preview
              }}
            >
              {item.filename}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
