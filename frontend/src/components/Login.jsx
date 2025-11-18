"use client"

import { useState } from "react"

export default function Login({ authApi, onLogin }) {
  const [mode, setMode] = useState("login")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const [message, setMessage] = useState("")

  async function submit(e) {
    e.preventDefault()
    setLoading(true)
    setError("")
    setMessage("")
    try {
      if (mode === "register") {
        const resp = await fetch(`${authApi}/api/auth/register`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, password }),
        })
        const data = await resp.json()
        if (!resp.ok) throw new Error(data.error || "Registration failed")
        setMessage("Registered! You can now log in.")
        setMode("login")
      } else {
        const resp = await fetch(`${authApi}/api/auth/login`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, password }),
        })
        const data = await resp.json()
        if (!resp.ok) throw new Error(data.error || "Login failed")
        onLogin(data.token)
      }
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card" style={{ maxWidth: 420, width: "100%", margin: "0 auto" }}>
      <div style={{ display: "flex", gap: "0.5rem", marginBottom: "1rem", flexWrap: "wrap" }}>
        <button className={`button ${mode === "login" ? "" : "secondary"}`} onClick={() => setMode("login")} style={{ flex: "1 1 120px" }}>
          Login
        </button>
        <button className={`button ${mode === "register" ? "" : "secondary"}`} onClick={() => setMode("register")} style={{ flex: "1 1 120px" }}>
          Register
        </button>
      </div>
      <form onSubmit={submit}>
        <label className="help" htmlFor="email">
          Email
        </label>
        <input
          id="email"
          className="input"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <label className="help" htmlFor="pwd" style={{ marginTop: "0.75rem" }}>
          Password
        </label>
        <input
          id="pwd"
          className="input"
          type="password"
          minLength={8}
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button className="button" style={{ marginTop: "0.9rem" }} disabled={loading}>
          {loading
            ? mode === "register"
              ? "Registering..."
              : "Logging in..."
            : mode === "register"
              ? "Create account"
              : "Login"}
        </button>
        {error && (
          <p className="help" style={{ color: "var(--primary)", marginTop: "0.5rem" }}>
            {error}
          </p>
        )}
        {message && (
          <p className="help" style={{ color: "var(--accent)", marginTop: "0.5rem" }}>
            {message}
          </p>
        )}
      </form>
    </div>
  )
}
