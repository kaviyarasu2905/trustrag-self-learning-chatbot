import PropTypes from 'prop-types'

export default function TrustScoreDisplay({ trustScore, confidenceScore }) {
  const getColor = (score) => {
    if (score >= 0.67) return '#27ae60' // Green
    if (score >= 0.34) return '#f39c12' // Yellow
    return '#e74c3c' // Red
  }

  const getLabel = (score) => {
    if (score >= 0.67) return 'High Trust'
    if (score >= 0.34) return 'Medium Trust'
    return 'Low Trust'
  }

  const color = getColor(trustScore)
  const label = getLabel(trustScore)
  const circumference = 2 * Math.PI * 45
  const offset = circumference - (trustScore / 1.0) * circumference

  return (
    <div className="trust-score-container">
      <svg className="gauge" viewBox="0 0 100 100">
        <circle cx="50" cy="50" r="45" fill="none" stroke="#e0e0e0" strokeWidth="8" />
        <circle
          cx="50"
          cy="50"
          r="45"
          fill="none"
          stroke={color}
          strokeWidth="8"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          style={{ transition: 'stroke-dashoffset 0.5s ease' }}
        />
        <text x="50" y="60" textAnchor="middle" fontSize="24" fontWeight="bold" fill={color}>
          {trustScore.toFixed(2)}
        </text>
      </svg>
      <div>
        <p className="font-bold text-gray-800">{label}</p>
        <p className="text-sm text-gray-600">Confidence: {(confidenceScore * 100).toFixed(0)}%</p>
      </div>
    </div>
  )
}

TrustScoreDisplay.propTypes = {
  trustScore: PropTypes.number.isRequired,
  confidenceScore: PropTypes.number.isRequired,
}
