"use client";
import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { CircularProgress } from "@mui/material";
import { FaCalendarAlt, FaNewspaper, FaRobot } from "react-icons/fa";

export default function LandingPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [scheduledTime, setScheduledTime] = useState("");
  const [category, setCategory] = useState("space"); // Default category
  const [prompt, setPrompt] = useState("");
  const [generatedBlog, setGeneratedBlog] = useState("");

  const handleLoginRedirect = () => {
    setLoading(true);
    alert("Redirecting to login...");
    setTimeout(() => {
      router.push("/login"); // Redirect to the login page
    }, 2000); // Simulate a delay for the spinner
  };

  const handleScheduleBlog = async () => {
    setLoading(true);
    try {
      const accessToken = localStorage.getItem("accessToken");
      if (!accessToken) {
        alert("Please login to schedule a blog.");
        router.push("/login");
        return;
      }

      await fetch("/api/schedules/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
        body: JSON.stringify({ scheduled_time: scheduledTime, preferences: { category } }),
      });
      alert("Blog scheduled successfully!");
    } catch (error) {
      alert("Failed to schedule blog. Please try again.");
      console.error("Schedule error", error);
    } finally {
      setLoading(false);
    }
  };

  const handleGeneratePrompt = async () => {
    setLoading(true);
    try {
      const accessToken = localStorage.getItem("accessToken");
      if (!accessToken) {
        alert("Please login to generate a blog.");
        router.push("/login");
        return;
      }
      const response = await fetch('/api/generate-prompt', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${accessToken}`,
        },
        body: JSON.stringify({ prompt }),
      });

      const data = await response.json();
      setGeneratedBlog(data.generated_text);

    } catch (error) {
      alert("Failed to generate blog.");
      console.error("Generate error", error);
    } finally {
      setLoading(false);
    }

  };

  return (
    <div className="flex flex-col min-h-screen">
      {/* Header */}
      <header className="bg-blue-700 text-white py-5 shadow-lg">
        <div className="container mx-auto flex justify-between items-center px-6">
          <h1 className="text-3xl font-extrabold">AI Blog Generator</h1>
          <nav>
            <ul className="flex space-x-6 text-lg">
              <li>
                <a href="#features" className="hover:underline">
                  Features
                </a>
              </li>
              <li>
                <a href="#footer" className="hover:underline">
                  About
                </a>
              </li>
            </ul>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-grow bg-gray-100">
        <div className="container mx-auto text-center py-24 px-6">
          <h2 className="text-5xl font-bold text-gray-900 mb-6">
            Generate AI-Powered Blogs
          </h2>
          <p className="text-lg text-gray-700 mb-8 max-w-2xl mx-auto">
            Create engaging and informative blog posts with the power of AI.
          </p>
          <div className="flex justify-center">
            <button
              onClick={handleLoginRedirect}
              className="bg-blue-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-blue-700 flex items-center justify-center transition-all duration-300 shadow-md"
              disabled={loading}
            >
              {loading ? (
                <>
                  <CircularProgress size={24} color="inherit" />
                  <span className="ml-2">Processing...</span>
                </>
              ) : (
                "Get Started"
              )}
            </button>
          </div>
        </div>

        {/* Features Section */}
        <section id="features" className="container mx-auto py-20 px-6">
          <h3 className="text-4xl font-bold text-center mb-10 text-gray-900">
            Blog Generation Features
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="p-6 bg-white rounded-xl shadow-lg flex flex-col items-center text-center hover:shadow-2xl transition-shadow duration-300">
              <FaCalendarAlt size={40} className="text-blue-600 mb-4" />
              <h4 className="text-xl font-semibold">Schedule Blogs</h4>
              <p className="text-gray-600 mt-3">
                Schedule your blog posts to be generated at specific times.
              </p>
            </div>
            <div className="p-6 bg-white rounded-xl shadow-lg flex flex-col items-center text-center hover:shadow-2xl transition-shadow duration-300">
              <FaNewspaper size={40} className="text-green-600 mb-4" />
              <h4 className="text-xl font-semibold">Category Selection</h4>
              <p className="text-gray-600 mt-3">
                Choose from various categories like space, news, sports, and more.
              </p>
            </div>
            <div className="p-6 bg-white rounded-xl shadow-lg flex flex-col items-center text-center hover:shadow-2xl transition-shadow duration-300">
              <FaRobot size={40} className="text-purple-600 mb-4" />
              <h4 className="text-xl font-semibold">AI Prompt Input</h4>
              <p className="text-gray-600 mt-3">
                Enter custom prompts for tailored blog content.
              </p>
            </div>
          </div>
        </section>

        {/* Scheduling and Prompt Section */}
        <section className="container mx-auto py-10 px-6">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-2xl font-semibold mb-4">Schedule Your Blog</h3>
            <input
              type="datetime-local"
              value={scheduledTime}
              onChange={(e) => setScheduledTime(e.target.value)}
              className="w-full p-2 mb-4 border rounded"
            />
            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-bold mb-2">Select Category:</label>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="w-full p-2 border rounded"
              >
                <option value="space">Space</option>
                <option value="news">News</option>
                <option value="sports">Sports</option>
                <option value="economy">Economy</option>
                <option value="entertainment">Entertainment</option>
              </select>
            </div>
            <button
              onClick={handleScheduleBlog}
              className="bg-green-600 text-white px-4 py-2 rounded-lg"
              disabled={loading}
            >
              {loading ? <><CircularProgress size={20} color="inherit" /> Processing...</> : "Schedule"}
            </button>
          </div>
          <div className="mt-8 bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-2xl font-semibold mb-4">Generate Blog Prompt</h3>
            <textarea
              placeholder="Enter your prompt here..."
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              className="w-full p-2 mb-4 border rounded"
            />
            <button
              onClick={handleGeneratePrompt}
              className="bg-purple-600 text-white px-4 py-2 rounded-lg"
              disabled={loading}
            >
              {loading ? <><CircularProgress size={20} color="inherit" /> Processing...</> : "Generate"}
            </button>
            {generatedBlog && <div className="mt-4">
              <p className="font-semibold">Generated Blog:</p>
              <p>{generatedBlog}</p>
            </div>}
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer id="footer" className="bg-gray-900 text-white py-8">
        <div className="container mx-auto text-center">
          <p className="text-lg font-light">
            &copy; {new Date().getFullYear()} AI Blog Generator. All rights reserved.
          </p>
          <p className="text-sm mt-2">
            <a href="#privacy" className="hover:underline">
              Privacy Policy
            </a>{" "}
            |{" "}
            <a href="#terms" className="hover:underline">
              Terms of Service
            </a>
          </p>
        </div>
      </footer>
    </div>
  );
}