import { useState } from "react";

export default function UploadForm() {
  const [title, setTitle] = useState("");
  const [file, setFile] = useState(null);

  function handleSubmit(e) {
    e.preventDefault();

    if (!title || !file) {
      alert("Please enter a title and select a file.");
      return;
    }

    // For now, mock the upload process
    console.log("Uploading:", { title, file });
    alert(`Uploaded "${title}" successfully!`);

    // Reset form
    setTitle("");
    setFile(null);
    e.target.reset();
  }

  return (
    <form onSubmit={handleSubmit} style={{ maxWidth: "400px", margin: "auto" }}>
      <h2>Upload Document</h2>

      <label>Title:</label>
      <input
        type="text"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Enter document title"
        required
      />

      <label>File:</label>
      <input
        type="file"
        accept=".jpg,.jpeg,.png"
        onChange={(e) => setFile(e.target.files[0])}
        required
      />

      <button type="submit">Upload</button>
    </form>
  );
}
