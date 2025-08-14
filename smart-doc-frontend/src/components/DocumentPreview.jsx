export default function DocumentPreview() {
  return (
    <div className="flex flex-col items-center text-center">
      <svg
        style={{ width: "48px", height: "48px" }}
        xmlns="http://www.w3.org/2000/svg"
        className="w-12 h-12 text-gray-400"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth="2"
          d="M15 10l4.553-4.553a2.121 2.121 0 013 3L18 13m-3-3a6 6 0 11-9.9 2.1"
        />
      </svg>
      <h2 className="mt-4 text-lg font-semibold">Document Preview</h2>
      <p className="text-gray-500 text-sm">
        Enter a document name to fetch and preview content
      </p>
    </div>
  );
}

