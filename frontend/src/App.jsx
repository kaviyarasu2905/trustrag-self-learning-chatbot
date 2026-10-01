import { useState, useCallback } from 'react'
import ChatInterface from './components/ChatInterface'
import ResponseDisplay from './components/ResponseDisplay'
import TrustScoreDisplay from './components/TrustScoreDisplay'
import SourceCitations from './components/SourceCitations'
import VerificationBadge from './components/VerificationBadge'
import LoadingSpinner from './components/LoadingSpinner'
import { sendQuery, submitFeedback } from './services/api'
import './App.css'

export default function App() {
  const [messages, setMessages] = useState([])
  const [currentQuery, setCurrentQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const [lastResponse, setLastResponse] = useState(null)

  const handleSendQuery = useCallback(async () => {
    if (!currentQuery.trim() || loading) return

    const query = currentQuery.trim()
    setCurrentQuery('')
    setLoading(true)

    const response = await sendQuery(query)
    setLastResponse(response)

    setMessages(prev => [...prev, {
      query,
      answer: response.answer,
      trustScore: response.trust_score,
      confidenceScore: response.confidence_score,
      sources: response.sources,
      verificationStatus: response.verification_status,
      timestamp: response.timestamp,
    }])

    setLoading(false)
  }, [currentQuery, loading])

  const handleFeedback = async (rating) => {
    if (lastResponse && messages.length > 0) {
      await submitFeedback(messages.length - 1, rating, '')
    }
  }

  return (
    <div className="app-container">
      <div className="app-header">
        <h1>🤖 TrustRAG</h1>
        <p>Reliable AI Chatbot with Verified Responses</p>
      </div>

      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', minHeight: 0 }}>
        <div style={{ flex: 1, overflow: 'hidden' }}>
          <ChatInterface
            messages={messages}
            currentQuery={currentQuery}
            loading={loading}
            onQueryChange={setCurrentQuery}
            onSendQuery={handleSendQuery}
          />
        </div>
      </div>

      {lastResponse && !loading && (
        <div className="px-6 pb-6 bg-white rounded-lg shadow">
          <LoadingSpinner isLoading={loading} />
          <ResponseDisplay
            answer={lastResponse.answer}
            timestamp={lastResponse.timestamp}
            isLoading={loading}
          />
          <TrustScoreDisplay
            trustScore={lastResponse.trust_score}
            confidenceScore={lastResponse.confidence_score}
          />
          <VerificationBadge
            status={lastResponse.verification_status}
            txHash={lastResponse.txHash}
          />
          <SourceCitations sources={lastResponse.sources} />
          
          <div className="flex gap-2 mt-4">
            <button
              onClick={() => handleFeedback(5)}
              className="px-4 py-2 bg-green-500 text-white rounded text-sm hover:bg-green-600 transition"
            >
              👍 Helpful
            </button>
            <button
              onClick={() => handleFeedback(1)}
              className="px-4 py-2 bg-red-500 text-white rounded text-sm hover:bg-red-600 transition"
            >
              👎 Not Helpful
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
