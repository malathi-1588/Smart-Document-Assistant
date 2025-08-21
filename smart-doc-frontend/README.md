# Smart Document Assistant – Frontend

This is the **frontend** of the **Smart Document Assistant**, a web app that allows users to:
- 📤 Upload documents  
- 📂 Fetch documents by name  
- 👀 Preview uploaded documents  

The project is built with **React + Vite** and styled using **Tailwind CSS**.  

---

## Features
**User Authentication:** Login and Signup functionality.
**Document Upload:** Upload documents to the server.
**Document Fetch:** Search and fetch documents by name.
**Document Preview:** View document details and content.
**Text Extraction:** Display extracted text from uploaded documents.
**Responsive Design:** Works well on desktop and mobile devices.

---

## Folder Structure
```bash
smart-doc-frontend/
├── public/                # Static assets
├── src/
│   ├── assets/            # Images and icons
│   ├── components/        # React components
│   │   ├── DocumentFetch.jsx
│   │   ├── DocumentPreview.jsx
│   │   ├── DocumentText.jsx
│   │   ├── DocumentUpload.jsx
│   │   ├── Login.jsx
│   │   └── Signup.jsx
│   ├── App.jsx            # Main app component
│   ├── App.css            # App-specific styles
│   ├── index.css          # Global styles
│   └── main.jsx           # Entry point
├── index.html             # HTML template
├── package.json           # Project metadata and scripts
├── tailwind.config.js     # Tailwind CSS configuration
├── postcss.config.js      # PostCSS configuration
├── vite.config.js         # Vite configuration
└── README.md              # Project documentation
```
---

## 🚀 Tech Stack

- [React](https://reactjs.org/) (with [Vite](https://vitejs.dev/) bundler)  
- [Tailwind CSS](https://tailwindcss.com/) for styling  

Components included:
- `DocumentUpload` → Upload PDF files  
- `DocumentFetch` → Retrieve uploaded files  
- `DocumentPreview` → Display file contents  

---

## ⚙️ Setup & Installation

   ```bash
   git clone https://github.com/malathi-1588/smart-doc-frontend.git
   cd smart-doc-frontend
   npm install
   npm run dev
```

The app will run on http://localhost:5173

---

## Usage
**Login/Signup:**
Create an account or log in to access document features.
**Upload Document:**
Use the upload form to select and upload a document.
**Fetch Document:**
Search for documents by name.
**Preview & Extracted Text:**
View document details and extracted text in the preview section.

