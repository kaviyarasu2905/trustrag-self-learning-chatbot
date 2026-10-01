import { useState } from 'react'
import PropTypes from 'prop-types'
import { FiCopy, FiChevronDown, FiChevronUp } from 'react-icons/fi'

export default function SourceCitations({ sources }) {
  const [expanded, setExpanded] = useState(false)

  if (!sources || sources.length === 0) {
    return <p className="text-xs text-gray-500">No sources available</p>
  }

  const handleCopy = () => {
    const citation = sources
      .map(s => `${s.docId} (${s.similarity.toFixed(2)})`)
      .join(', ')
    navigator.clipboard.writeText(citation)
  }

  const topSource = sources[0]

  return (
    <div className="mt-3 border-t pt-3">
      <div className="flex items-center justify-between gap-2">
        <div className="flex items-center gap-2 flex-1">
          <span className="text-xs font-bold text-gray-700">Sources:</span>
          <span className="text-xs text-gray-600">
            {sources.map((s, i) => (
              <span key={i}>
                {s.docId} ({s.similarity.toFixed(2)})
                {i < sources.length - 1 ? ', ' : ''}
              </span>
            ))}
          </span>
          {topSource && (
            <span className="inline-block px-2 py-1 bg-green-100 text-green-800 text-xs rounded font-bold">
              Top Match
            </span>
          )}
        </div>
        <button
          onClick={handleCopy}
          className="text-blue-500 hover:text-blue-700 transition"
          title="Copy to clipboard"
        >
          <FiCopy size={14} />
        </button>
        <button
          onClick={() => setExpanded(!expanded)}
          className="text-gray-500 hover:text-gray-700 transition"
        >
          {expanded ? <FiChevronUp size={14} /> : <FiChevronDown size={14} />}
        </button>
      </div>

      {expanded && (
        <div className="mt-2 p-2 bg-gray-50 rounded border border-gray-200">
          {sources.map((source, i) => (
            <div key={i} className="text-xs text-gray-700 mb-2 pb-2 border-b last:border-b-0">
              <p className="font-bold">{source.docId} (Similarity: {(source.similarity * 100).toFixed(1)}%)</p>
              <p className="text-gray-600 italic">{source.content || 'Document content not available'}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

SourceCitations.propTypes = {
  sources: PropTypes.arrayOf(
    PropTypes.shape({
      docId: PropTypes.string.isRequired,
      similarity: PropTypes.number.isRequired,
      content: PropTypes.string,
    })
  ).isRequired,
}
