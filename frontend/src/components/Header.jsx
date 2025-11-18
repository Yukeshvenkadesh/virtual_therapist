"use client"

import { NavLink } from "react-router-dom"

export default function Header({ dark, setDark }) {
  return (
    <header className="header">
      <div className="header-inner">
        <div className="brand">
          <img src="/logo.png" alt="Virtual Therapist logo" />
          <span>Virtual Therapist</span>
        </div>
        <nav className="nav" aria-label="Primary">
          <NavLink to="/" className={({ isActive }) => (isActive ? "active" : "")}>
            Individual
          </NavLink>
          <NavLink to="/pro" className={({ isActive }) => (isActive ? "active" : "")}>
            For Professionals
          </NavLink>
        </nav>
        <label className="toggle" title="Toggle dark mode">
          <input type="checkbox" checked={dark} onChange={() => setDark((v) => !v)} aria-label="Dark mode" />
          <span>Dark</span>
          <span className="dot" aria-hidden="true"></span>
        </label>
      </div>
    </header>
  )
}
