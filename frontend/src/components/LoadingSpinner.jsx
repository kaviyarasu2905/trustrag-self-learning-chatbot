import PropTypes from 'prop-types'

export default function LoadingSpinner({ isLoading }) {
  if (!isLoading) return null

  return (
    <div className="flex items-center gap-3 p-4 bg-blue-50 rounded-lg border border-blue-200">
      <div className="loading-spinner"></div>
      <span className="text-gray-600 text-sm">Generating answer...</span>
    </div>
  )
}

LoadingSpinner.propTypes = {
  isLoading: PropTypes.bool.isRequired,
}
