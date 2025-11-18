import ConfidenceChart from "./ConfidenceChart.jsx"

export default function ResultCard({ result }) {
  if (!result) return null
  return (
    <div className="card">
      <div className="result-title">Top Pattern: {result.topPattern}</div>
      <ConfidenceChart scores={result.confidenceScores} />
    </div>
  )
}
