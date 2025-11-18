import { Router } from "express"
import jwt from "jsonwebtoken"
import User from "../models/User.js"

const router = Router()

router.post("/register", async (req, res) => {
  try {
    const { email, password } = req.body
    if (!email || !password) return res.status(400).json({ error: "Email and password required" })

    const existing = await User.findOne({ email })
    if (existing) return res.status(409).json({ error: "User already exists" })

    const user = new User({ email, password })
    await user.save()
    return res.status(201).json({ message: "Registered successfully" })
  } catch (err) {
    console.error("[register] error:", err)
    return res.status(500).json({ error: "Server error" })
  }
})

router.post("/login", async (req, res) => {
  try {
    const { email, password } = req.body
    if (!email || !password) return res.status(400).json({ error: "Email and password required" })

    const user = await User.findOne({ email })
    if (!user) return res.status(401).json({ error: "Invalid credentials" })

    const valid = await user.comparePassword(password)
    if (!valid) return res.status(401).json({ error: "Invalid credentials" })

    const token = jwt.sign({ id: user._id }, process.env.JWT_SECRET, { expiresIn: "7d" })
    return res.json({ token })
  } catch (err) {
    console.error("[login] error:", err)
    return res.status(500).json({ error: "Server error" })
  }
})

export default router
