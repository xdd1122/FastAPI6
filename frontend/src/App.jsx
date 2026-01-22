import { Routes, Route, Link } from "react-router-dom";

import Register from "./pages/Register";
import Login from "./pages/Login";
import ListUsers from "./pages/UsersList";
import Home from "./pages/Home";

import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useEffect } from 'react';

const GITHUB_AUTH_URL = "http://localhost:8000/auth/github/login"; // backend GitHub login URL


function OAuthCallbackHandler() {
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const token = params.get("token");

    if (token) {
      localStorage.setItem("token", token);
      navigate("/");
    } else {
      navigate("/login");
    }
  }, [location, navigate]);

  return <p>Processing login...</p>;
}

export default function App() {
  // 2. Add Hooks here to enable global token checking
  const location = useLocation();
  const navigate = useNavigate();

  // 3. GLOBAL TOKEN CATCHER
  // This watches every page load. If it sees "?token=" (even on Home), it saves it.
  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const token = params.get("token");

    if (token) {
      console.log("Global Token Catcher: Found token in URL!");
      
      // Save to localStorage
      localStorage.setItem("token", token);
      
      // Remove the token from the URL so it looks clean (redirects to same page without params)
      // This prevents the token from sitting in the address bar
      window.history.replaceState({}, document.title, window.location.pathname);
      
      // Optional: Refresh or navigate to ensure state updates
      navigate("/"); 
    }
  }, [location, navigate]);

  return (
    <div className="p-6 font-sans">
      <div className="mt-16" />
      <nav className="space-x-4 mb-6">
        <Link to="/" className="text-blue-600 hover:underline">Home</Link>
        &nbsp; &nbsp;
        <Link to="/register" className="text-blue-600 hover:underline">Register</Link>
        &nbsp; &nbsp; 
        <Link to="/login" className="text-blue-600 hover:underline">Login</Link>
        &nbsp; &nbsp; 
        <Link to="/users" className="text-blue-600 hover:underline">Users</Link>
        &nbsp; &nbsp; 
        {/* 4. Connect the button to the constant we defined above */}
        <button
          onClick={() => window.location.href = GITHUB_AUTH_URL}
          className="text-white bg-black px-3 py-1 rounded hover:bg-gray-800 ml-4"
        >
          Login with GitHub
        </button>
      </nav>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/users" element={<ListUsers />} />
        <Route path="/oauth/callback" element={<OAuthCallbackHandler />} />
      </Routes>
    </div>
  );
}