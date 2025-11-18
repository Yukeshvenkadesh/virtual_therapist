"use client"

import { useEffect, useState } from "react"
import Login from "./Login.jsx"
import Dashboard from "./Dashboard.jsx"
import { Routes, Route, Navigate, useNavigate } from "react-router-dom"

function hasToken() {
  return !!localStorage.getItem("vt_token")
}

export default function PsychologistView({ authApi }) {
  const [authed, setAuthed] = useState(hasToken())
  const navigate = useNavigate()

  useEffect(() => {
    const onStorage = () => setAuthed(hasToken())
    window.addEventListener("storage", onStorage)
    return () => window.removeEventListener("storage", onStorage)
  }, [])

  function onLogin(token) {
    localStorage.setItem("vt_token", token)
    setAuthed(true)
    navigate("/pro/dashboard", { replace: true })
  }
  function onLogout() {
    localStorage.removeItem("vt_token")
    setAuthed(false)
    navigate("/pro", { replace: true })
  }

  return (
    <Routes>
      <Route
        index
        element={authed ? <Navigate to="dashboard" replace /> : <Login authApi={authApi} onLogin={onLogin} />}
      />
      <Route
        path="dashboard"
        element={authed ? <Dashboard authApi={authApi} onLogout={onLogout} /> : <Navigate to="/pro" replace />}
      />
      <Route path="*" element={<Navigate to="/pro" replace />} />
    </Routes>
  )
}
