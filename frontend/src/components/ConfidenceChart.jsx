export default function ConfidenceChart({ scores }) {
  if (!scores || scores.length === 0) return null
  const max = Math.max(...scores.map((s) => s.score), 1)
  return (
    <div className="chart" role="img" aria-label="Confidence scores">
      {scores.map((s) => (
        <div className="bar" key={s.label}>
          <div className="bar-label">{s.label}</div>
          <div className="bar-track" aria-hidden="true">
            <div className="bar-fill" style={{ width: `${Math.max(2, (s.score / max) * 100)}%` }} />
          </div>
          <div className="bar-percentage">{(s.score * 100).toFixed(0)}%</div>
        </div>
      ))}
    </div>
  )
}
