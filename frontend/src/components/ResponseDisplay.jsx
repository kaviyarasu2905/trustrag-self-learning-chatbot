import PropTypes from 'prop-types'

export default function ResponseDisplay({ answer, timestamp, isLoading }) {
  if (isLoading) {
    return (
      <div className="response-card">
        <div className="loading-spinner" style={{ marginRight: '8px' }}></div>
        <span className="text-gray-600 text-sm">Generating answer...</span>
      </div>
    )
  }

  if (!answer) return null

  return (
    <div className="response-card fade-in">
      <div className="flex justify-between items-start mb-2">
        <h3 className="font-bold text-gray-800">Answer</h3>
        {timestamp && (
          <span className="text-xs text-gray-500">{new Date(timestamp).toLocaleTimeString()}</span>
        )}
      </div>
      <p className="text-gray-700 text-sm leading-relaxed whitespace-pre-wrap">{answer}</p>
    </div>
  )
}

ResponseDisplay.propTypes = {
  answer: PropTypes.string,
  timestamp: PropTypes.string,
  isLoading: PropTypes.bool,
}

ResponseDisplay.defaultProps = {
  isLoading: false,
}
