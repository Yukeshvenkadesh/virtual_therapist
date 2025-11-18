import { Router } from "express"
import UserSession from "../models/UserSession.js"
import fetch from "node-fetch"

const router = Router()

// Create or get session
router.post("/", async (req, res) => {
  try {
    const sessionId = req.body.sessionId || `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    
    let session = await UserSession.findOne({ sessionId })
    if (!session) {
      session = new UserSession({ sessionId })
      await session.save()
    } else {
      // Update last accessed time
      session.lastAccessed = new Date()
      await session.save()
    }
    
    return res.json({ sessionId: session.sessionId })
  } catch (err) {
    console.error("[sessions POST] error:", err)
    return res.status(500).json({ error: "Server error" })
  }
})

// Analyze text for individual user
router.post("/:sessionId/analyze", async (req, res) => {
  try {
    const { sessionId } = req.params
    const { text } = req.body
    
    if (!text || text.trim().length < 5) {
      return res.status(400).json({ error: "Text is too short" })
    }

    let session = await UserSession.findOne({ sessionId })
    if (!session) {
      return res.status(404).json({ error: "Session not found" })
    }

    // Call model service; treat env as base and append /api/analyze
    const analysisBase = process.env.ANALYSIS_SERVICE_URL || "http://localhost:5002"
    const analysisUrl = `${analysisBase.replace(/\/$/, '')}/api/analyze`
    const response = await fetch(analysisUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    })

    if (!response.ok) {
      console.error("[session analyze] analysis service error:", response.status)
      return res.status(502).json({ error: "Analysis service unavailable" })
    }

    const result = await response.json()
    
    // Store analysis in session
    const analysis = {
      text,
      topPattern: result.topPattern,
      confidenceScores: result.confidenceScores,
      createdAt: new Date(),
    }
    
    session.analyses.unshift(analysis)
    session.lastAccessed = new Date()
    
    // Keep only last 50 analyses per session
    if (session.analyses.length > 50) {
      session.analyses = session.analyses.slice(0, 50)
    }
    
    await session.save()
    
    return res.json({ analysis, sessionId: session.sessionId })
  } catch (err) {
    console.error("[session analyze] error:", err)
    return res.status(500).json({ error: "Server error" })
  }
})

// Get session history
router.get("/:sessionId/history", async (req, res) => {
  try {
    const { sessionId } = req.params
    const session = await UserSession.findOne({ sessionId })
    
    if (!session) {
      return res.status(404).json({ error: "Session not found" })
    }
    
    // Update last accessed time
    session.lastAccessed = new Date()
    await session.save()
    
    return res.json({ analyses: session.analyses })
  } catch (err) {
    console.error("[session history] error:", err)
    return res.status(500).json({ error: "Server error" })
  }
})

// Clear session data
router.delete("/:sessionId", async (req, res) => {
  try {
    const { sessionId } = req.params
    await UserSession.deleteOne({ sessionId })
    return res.json({ message: "Session cleared" })
  } catch (err) {
    console.error("[session delete] error:", err)
    return res.status(500).json({ error: "Server error" })
  }
})

export default router

