import { useState } from "react";
export default function Login({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async () => {
    try {
      const res = await fetch("http://localhost:5000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });
      const data = await res.json();
      if (res.ok) {
        onLogin(data);
      } else {
        setError(data.error || "Login failed");
      }
    } catch {
      setError("Server error");
    }
  };

  return (
    <div className="bg-white p-8 rounded-2xl shadow-xl w-80">
      <h2 className="text-2xl font-bold mb-6 text-gray-800 text-center">Login</h2>
      {error && <p className="text-red-500 mb-2">{error}</p>}
        <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        className="w-full border rounded p-2 mb-3 text-black"
      />
        <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        className="w-full border rounded p-2 mb-3 text-black"
      />
        <button
        onClick={handleLogin}
        className="w-full bg-black text-white py-2 rounded hover:bg-gray-800"
      >
          Login
        </button>
    </div>
  );
}
