"use client"; // Required for Next.js 14+ client components

import { useEffect, useState } from "react";

function StoryComponent() {
    const [story, setStory] = useState("Waiting for today's story...");

    useEffect(() => {
        const socket = new WebSocket("ws://localhost:8000/ws/stories/");

        socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            setStory(data.story);
        };

        return () => socket.close();
    }, []);

    return (
        <div className="flex flex-col items-center justify-center h-screen bg-gray-100 w-full">
            <h1 className="text-3xl font-bold mb-4">Daily Story</h1>
            <p className="text-lg text-gray-700 bg-white shadow-md p-6 rounded-lg">{story}</p>
        </div>
    );
}

export default StoryComponent;
