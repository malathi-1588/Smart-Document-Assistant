import DocumentUpload from "./components/DocumentUpload";
import DocumentPreview from "./components/DocumentPreview";
import DocumentFetch from "./components/DocumentFetch";

export default function App() {
  return (
    <div className="min-h-screen min-w-screen bg-gray-100 p-8">
      <div className="max-w-7xl mx-auto px-2">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Smart Document Assistant
        </h1>
        <p className="text-gray-600 mb-10">
          Upload documents or fetch them by name to access content and insights
        </p>

        {/* Upload + Fetch (left) and Preview (right) */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Left side: Upload + Fetch */}
          <div className="flex flex-col gap-8 md:col-span-2">
            <div className="bg-white rounded-xl shadow p-6">
              <DocumentUpload />
            </div>
            <div className="bg-white rounded-xl shadow p-6">
              <DocumentFetch />
            </div>
          </div>

          {/* Right side: Preview */}
          <div className="bg-white rounded-xl shadow p-6 md:col-span-2">
            <DocumentPreview />
          </div>
        </div>
      </div>
    </div>
  );
}


// export default function App() {
//   return (
//     <div className="min-h-screen min-w-screen bg-gray-100 p-8">
//       <div className="max-w-7xl mx-auto">
//         <h1 className="text-3xl font-bold text-gray-900 mb-2">
//           Smart Document Assistant
//         </h1>
//         <p className="text-gray-600 mb-10">
//           Upload documents or fetch them by name to access content and insights
//         </p>

//         {/* Upload + Fetch (left) and Preview (right) */}
//         <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
//           {/* Left side: Upload + Fetch */}
//           <div className="flex flex-col gap-8 md:col-span-1">
//             <div className="bg-white rounded-xl shadow p-6">
//               <DocumentUpload />
//             </div>
//             <div className="bg-white rounded-xl shadow p-6">
//               <DocumentFetch />
//             </div>
//           </div>

//           {/* Right side: Preview (larger) */}
//           <div className="bg-white rounded-xl shadow p-6 md:col-span-2">
//             <DocumentPreview />
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// }


