"use client"

import { useEffect, useMemo, useState } from "react"
import ResultCard from "./ResultCard.jsx"

function useAuthHeaders() {
  const token = localStorage.getItem("vt_token") || ""
  return useMemo(() => ({ Authorization: `Bearer ${token}`, "Content-Type": "application/json" }), [token])
}

export default function Dashboard({ authApi, onLogout }) {
  const headers = useAuthHeaders()
  const [patients, setPatients] = useState([])
  const [selectedId, setSelectedId] = useState("")
  const [loadingList, setLoadingList] = useState(true)
  const [addingName, setAddingName] = useState("")
  const [submittingAdd, setSubmittingAdd] = useState(false)
  const [deleting, setDeleting] = useState(false)
  const [notes, setNotes] = useState("")
  const [analyzing, setAnalyzing] = useState(false)
  const [error, setError] = useState("")

  async function loadPatients() {
    setLoadingList(true)
    try {
      const resp = await fetch(`${authApi}/api/patients`, { headers })
      if (resp.status === 401) return onLogout()
      const data = await resp.json()
      setPatients(data)
      if (!selectedId && data.length > 0) setSelectedId(data[0]._id)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoadingList(false)
    }
  }

  useEffect(() => {
    loadPatients()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  async function addPatient() {
    if (!addingName.trim()) return
    setSubmittingAdd(true)
    setError("")
    try {
      const resp = await fetch(`${authApi}/api/patients`, {
        method: "POST",
        headers,
        body: JSON.stringify({ name: addingName.trim() }),
      })
      if (resp.status === 401) return onLogout()
      const data = await resp.json()
      if (!resp.ok) throw new Error(data.error || "Failed to add patient")
      setPatients((p) => [data, ...p])
      setSelectedId(data._id)
      setAddingName("")
    } catch (e) {
      setError(e.message)
    } finally {
      setSubmittingAdd(false)
    }
  }

  async function analyze() {
    if (!selectedId) return
    if (notes.trim().length < 5) {
      setError("Please enter at least 5 characters of session notes.")
      return
    }
    setAnalyzing(true)
    setError("")
    try {
      const resp = await fetch(`${authApi}/api/patients/${selectedId}/analyze`, {
        method: "POST",
        headers,
        body: JSON.stringify({ text: notes }),
      })
      if (resp.status === 401) return onLogout()
      const data = await resp.json()
      if (!resp.ok) throw new Error(data.error || "Analysis failed")
      setPatients((list) =>
        list.map((p) => (p._id === selectedId ? { ...p, history: [data.entry, ...(p.history || [])] } : p)),
      )
      setNotes("")
    } catch (e) {
      setError(e.message)
    } finally {
      setAnalyzing(false)
    }
  }

  async function deletePatient(id) {
    if (!id) return
    if (!confirm("Delete this patient? This cannot be undone.")) return
    setDeleting(true)
    setError("")
    try {
      const resp = await fetch(`${authApi}/api/patients/${id}`, {
        method: "DELETE",
        headers,
      })
      if (resp.status === 401) return onLogout()
      const data = await resp.json()
      if (!resp.ok) throw new Error(data.error || "Failed to delete patient")
      setPatients((list) => list.filter((p) => p._id !== id))
      if (selectedId === id) {
        const remaining = patients.filter((p) => p._id !== id)
        setSelectedId(remaining[0]?._id || "")
      }
    } catch (e) {
      setError(e.message)
    } finally {
      setDeleting(false)
    }
  }

  const selectedPatient = patients.find((p) => p._id === selectedId)

  return (
    <div className="row">
      <div className="col" style={{ maxWidth: 360, minWidth: 280 }}>
        <div className="card">
          <div className="result-title">Patients</div>
          <div style={{ marginTop: "0.5rem" }}>
            <label htmlFor="patientSelect" className="help">Quick switch</label>
            <select
              id="patientSelect"
              className="input"
              value={selectedId}
              onChange={(e) => setSelectedId(e.target.value)}
              disabled={patients.length === 0}
            >
              {patients.map((p) => (
                <option key={p._id} value={p._id}>{p.name}</option>
              ))}
            </select>
          </div>
          <div className="privacy-notice professional">
            <div className="privacy-icon">🏥</div>
            <div className="privacy-text">
              <strong>Professional Data:</strong> Patient data is stored securely for 30 days, then automatically deleted for privacy compliance.
            </div>
          </div>

          <div className="list" style={{ marginTop: "0.5rem", maxHeight: 320, overflow: "auto", border: "1px solid var(--border)", borderRadius: 8 }}>
            {loadingList && <div className="help">Loading...</div>}
            {!loadingList && patients.length === 0 && <div className="help">No patients yet.</div>}
            {patients.map((p) => (
              <button
                key={p._id}
                className="list-item"
                onClick={() => setSelectedId(p._id)}
                aria-pressed={selectedId === p._id}
                style={{ width: "100%", textAlign: "left", background: selectedId === p._id ? "var(--muted)" : undefined }}
              >
                <div>
                  <div style={{ fontWeight: 600 }}>{p.name}</div>
                  <div className="help">Created {new Date(p.createdAt).toLocaleDateString()}</div>
                </div>
                {selectedId === p._id && <span style={{ color: "var(--accent)", fontWeight: 700 }}>●</span>}
              </button>
            ))}
          </div>

          <div style={{ marginTop: "1rem" }}>
            <label className="help" htmlFor="pname">
              Add new patient
            </label>
            <input
              id="pname"
              className="input"
              value={addingName}
              onChange={(e) => setAddingName(e.target.value)}
              placeholder="Patient name"
            />
            <button className="button" style={{ marginTop: "0.5rem" }} onClick={addPatient} disabled={submittingAdd}>
              {submittingAdd ? "Adding..." : "Add Patient"}
            </button>
          </div>

          <button
            className="button secondary"
            style={{ marginTop: "0.5rem", background: "var(--muted)" }}
            onClick={() => deletePatient(selectedId)}
            disabled={!selectedId || deleting}
          >
            {deleting ? "Deleting..." : "Delete Selected"}
          </button>

          <button className="button secondary" style={{ marginTop: "1rem" }} onClick={onLogout}>
            Logout
          </button>
          {error && (
            <p className="help" style={{ color: "var(--primary)", marginTop: "0.5rem" }}>
              {error}
            </p>
          )}
        </div>
      </div>

      <div className="col">
        <div className="card">
          <div className="result-title">
            {selectedPatient ? `Analyze Session Notes — ${selectedPatient.name}` : "Select a patient"}
          </div>
          <textarea
            className="input"
            placeholder="Paste or type session notes..."
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            disabled={!selectedPatient}
          />
          <button
            className="button"
            style={{ marginTop: "0.75rem" }}
            onClick={analyze}
            disabled={!selectedPatient || analyzing}
          >
            {analyzing ? "Analyzing..." : "Analyze"}
          </button>
        </div>

        <div className="card" style={{ marginTop: "1rem" }}>
          <div className="result-title">Analysis History</div>
          {!selectedPatient || !selectedPatient.history || selectedPatient.history.length === 0 ? (
            <div className="help">No analysis history to display.</div>
          ) : (
            <div className="list" style={{ marginTop: "0.5rem", maxHeight: 360, overflow: "auto" }}>
              {selectedPatient.history.map((h, idx) => (
                <div key={idx} className="list-item" style={{ alignItems: "flex-start", flexDirection: "column", gap: "0.5rem" }}>
                  <div style={{ flex: 1, width: "100%" }}>
                    <div className="help">{new Date(h.createdAt).toLocaleString()}</div>
                    <div style={{ marginTop: 6, whiteSpace: "pre-wrap", wordBreak: "break-word" }}>{h.text}</div>
                    <div style={{ marginTop: 8 }}>
                      <ResultCard result={{ topPattern: h.topPattern, confidenceScores: h.confidenceScores }} />
                    </div>
                  </div>
                  <div style={{ fontWeight: 700, alignSelf: "flex-end" }}>{h.topPattern}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
