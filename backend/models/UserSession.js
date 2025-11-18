import mongoose from "mongoose"

// Schema for individual user sessions (temporary data)
const userSessionSchema = new mongoose.Schema(
  {
    sessionId: { type: String, required: true, unique: true },
    analyses: [
      {
        text: { type: String, required: true },
        topPattern: { type: String, required: true },
        confidenceScores: [
          {
            label: { type: String, required: true },
            score: { type: Number, required: true },
          },
        ],
        createdAt: { type: Date, default: Date.now },
      },
    ],
    lastAccessed: { type: Date, default: Date.now },
  },
  { timestamps: true },
)

// Auto-delete sessions after 1 hour of inactivity
userSessionSchema.index({ lastAccessed: 1 }, { expireAfterSeconds: 3600 })

export default mongoose.model("UserSession", userSessionSchema)

