"use client";

import { useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";
import { CircularProgress } from "@mui/material";

export default function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [username, setUsername] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter(); // Initialize the router

  const handleRegister = async () => {
    setLoading(true);
    try {
      await axios.post("http://127.0.0.1:8000/api/blogs/register/", {
        email,
        password,
        username,
      });
      alert("Registration successful! Please login.");
      router.push("/");
    } catch (error) {
      alert("Registration failed. Please check your details.");
      console.error("Registration Error", error);
    } finally {
      setLoading(false);
    }
  };

  const handleLoginNavigation = () => {
    router.push("/login"); // Navigate to the login page
  };

  return (
    <div className="flex items-center justify-center h-screen bg-gradient-to-r from-green-400 to-yellow-500">
      <div className="bg-white p-12 rounded-xl shadow-lg w-[600px] h-[600px] border border-gray-200 hover:shadow-2xl transition-shadow duration-300">
        <h2 className="text-4xl font-bold mb-8 text-center text-gray-800">Register</h2>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="w-full p-6 text-lg border border-gray-300 rounded-lg shadow-sm focus:ring-4 focus:ring-blue-500 focus:outline-none transition duration-300 mb-6"
        />

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full p-6 text-lg border border-gray-300 rounded-lg shadow-sm focus:ring-4 focus:ring-blue-500 focus:outline-none transition duration-300 mb-6"
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full p-6 text-lg border border-gray-300 rounded-lg shadow-sm focus:ring-4 focus:ring-blue-500 focus:outline-none transition duration-300 mb-6"
        />
        <button
          onClick={handleRegister}
          className="w-full bg-green-600 text-white py-4 text-lg rounded-lg shadow-md hover:bg-green-700 transition duration-300 flex justify-center items-center"
          disabled={loading}
        >
          {loading ? (
            <>
              <CircularProgress size={28} color="inherit" />
              <span className="ml-2">Processing...</span>
            </>
          ) : (
            "Register"
          )}
        </button>
        <div className="mt-4 text-center">
          <p>
            Have an account?{" "}
            <button onClick={handleLoginNavigation} className="text-blue-600 hover:underline">
              Login
            </button>
          </p>
        </div>
      </div>
    </div>
  );
}