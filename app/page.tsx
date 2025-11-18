"use client"

import { useEffect, useMemo, useState } from "react"
import { Routes, Route, Navigate, useLocation } from "react-router-dom"
import Header from "../frontend/src/components/Header.jsx"
import IndividualView from "../frontend/src/components/IndividualView.jsx"
import PsychologistView from "../frontend/src/components/PsychologistView.jsx"
import "../frontend/src/App.css"

export default function Page() {
  const [dark, setDark] = useState(() => {
    const saved = localStorage.getItem("vt_dark")
    return saved ? JSON.parse(saved) : true
  })
  useEffect(() => {
    localStorage.setItem("vt_dark", JSON.stringify(dark))
    document.documentElement.classList.toggle("dark", dark)
  }, [dark])

  const AUTH_API = process.env.NEXT_PUBLIC_AUTH_API_URL || "http://localhost:4000"
  const ANALYSIS_API = process.env.NEXT_PUBLIC_ANALYSIS_API_URL || "http://localhost:4000"

  const location = useLocation()
  const title = useMemo(() => {
    if (location.pathname.startsWith("/pro")) return "For Professionals"
    return "Individual"
  }, [location.pathname])

  return (
    <div className="app">
      <Header dark={dark} setDark={setDark} />
      <main className="container">
        <h1 className="page-title">{title}</h1>
        <Routes>
          <Route path="/" element={<IndividualView analysisApi={ANALYSIS_API} />} />
          <Route path="/pro/*" element={<PsychologistView authApi={AUTH_API} />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
      <footer className="footer">© {new Date().getFullYear()} Virtual Therapist</footer>
    </div>
  )
}
