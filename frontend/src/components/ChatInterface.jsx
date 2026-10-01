import { useEffect, useRef } from 'react'
import PropTypes from 'prop-types'
import { FiSend } from 'react-icons/fi'

export default function ChatInterface({ 
  messages, 
  currentQuery, 
  loading, 
  onQueryChange, 
  onSendQuery 
}) {
  const endRef = useRef(null)

  const scrollToBottom = () => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey && !loading) {
      onSendQuery()
    }
  }

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto chat-container">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full">
            <div className="text-center text-gray-500">
              <p className="text-lg font-bold mb-2">Welcome to TrustRAG</p>
              <p className="text-sm">Ask any question about university policies</p>
            </div>
          </div>
        ) : (
          messages.map((msg, idx) => (
            <div key={idx} className="message-group">
              {msg.query && (
                <div className="message-bubble user-message">
                  <p className="text-sm">{msg.query}</p>
                </div>
              )}
              {msg.answer && (
                <div className="message-bubble system-message">
                  <p className="text-sm">{msg.answer}</p>
                  {msg.trustScore && (
                    <p className="text-xs text-gray-500 mt-2">
                      Trust Score: {msg.trustScore.toFixed(2)}
                    </p>
                  )}
                </div>
              )}
            </div>
          ))
        )}
        <div ref={endRef} />
      </div>

      <div className="input-container">
        <textarea
          value={currentQuery}
          onChange={(e) => onQueryChange(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask a question about university policies..."
          className="query-input"
          disabled={loading}
          rows="2"
        />
        <button
          onClick={onSendQuery}
          disabled={loading || !currentQuery.trim()}
          className="send-button"
          title="Send query (Shift+Enter for new line)"
        >
          <FiSend size={18} />
        </button>
      </div>
    </div>
  )
}

ChatInterface.propTypes = {
  messages: PropTypes.arrayOf(PropTypes.object).isRequired,
  currentQuery: PropTypes.string.isRequired,
  loading: PropTypes.bool.isRequired,
  onQueryChange: PropTypes.func.isRequired,
  onSendQuery: PropTypes.func.isRequired,
}
