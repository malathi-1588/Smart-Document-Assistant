import { useState } from "react";

export default function Signup() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [msg, setMsg] = useState("");

  const handleSignup = async () => {
    try {
      const res = await fetch("http://localhost:5000/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });
      const data = await res.json();
      if (res.ok) {
        setMsg("✅ Signup successful, now login.");
      } else {
        setMsg(`❌ ${data.error}`);
      }
    } catch {
      setMsg("Server error");
    }
  };

  return (
    <div className="bg-white p-8 rounded-2xl shadow-xl w-80">
      <h2 className="text-2xl font-bold mb-6 text-gray-800 text-center">Sign Up</h2>
      {msg && <p className="mb-2 text-black">{msg}</p>}
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
        onClick={handleSignup}
        className="w-full bg-black text-white py-2 rounded hover:bg-gray-800"
      >
          Sign Up
        </button>
    </div>
  );
}
