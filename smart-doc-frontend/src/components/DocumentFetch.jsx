import { MagnifyingGlassIcon, ClockIcon } from "@heroicons/react/24/outline";
import { useState } from "react";

export default function DocumentFetch() {
  const [docName, setDocName] = useState("");
  const recentSearches = ["Financial Report 2024", "Project Plan Q3"];

  return (
    <div>
      <h2 className="text-lg font-semibold mb-4">Fetch Document</h2>

      {/* Search row */}
      <div className="flex">
        <input
          type="text"
          placeholder="Enter document name..."
          value={docName}
          onChange={(e) => setDocName(e.target.value)}
          className="flex-1 text-black bg-white border border-gray-300 rounded-l-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
        <button className="bg-blue-600 text-white px-4 py-2 rounded-r-lg hover:bg-blue-700 flex items-center justify-center">
          <MagnifyingGlassIcon className="w-5 h-5" />
        </button>
      </div>

      {/* Recent searches */}
      <div className="mt-4">
        <p className="text-gray-500 flex items-center gap-2">
          <ClockIcon className="w-4 h-4" /> Recent Searches
        </p>
        <ul className="mt-2 space-y-1">
          {recentSearches.map((item, index) => (
            <li
              key={index}
              className="text-blue-600 cursor-pointer hover:underline"
            >
              {item}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
