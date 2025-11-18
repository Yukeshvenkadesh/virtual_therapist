import mongoose from "mongoose"

const historySchema = new mongoose.Schema(
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
  { _id: false },
)

const patientSchema = new mongoose.Schema(
  {
    name: { type: String, required: true, trim: true },
    createdBy: { type: mongoose.Schema.Types.ObjectId, ref: "User", required: true },
    history: { type: [historySchema], default: [] },
    // Auto-delete patient data after 30 days
    expiresAt: { type: Date, default: () => new Date(Date.now() + 30 * 24 * 60 * 60 * 1000) },
  },
  { timestamps: true },
)

// TTL index for auto-deletion after 30 days
patientSchema.index({ expiresAt: 1 }, { expireAfterSeconds: 0 })

export default mongoose.model("Patient", patientSchema)
