import { useState } from 'react'
import PropTypes from 'prop-types'
import { FiCheckCircle, FiClock, FiLink2, FiAlertCircle, FiX } from 'react-icons/fi'

export default function VerificationBadge({ status, txHash, onViewTx }) {
  const [showModal, setShowModal] = useState(false)

  const statusConfig = {
    verified: {
      icon: FiCheckCircle,
      label: '✅ Verified & Accurate',
      color: 'bg-green-100 text-green-800',
      description: 'Answer verified by the Verifier Agent',
    },
    pending: {
      icon: FiClock,
      label: '⏳ Pending Human Review',
      color: 'bg-yellow-100 text-yellow-800',
      description: 'This query has been escalated to an administrator',
    },
    blockchain: {
      icon: FiLink2,
      label: '🔗 Blockchain Verified',
      color: 'bg-blue-100 text-blue-800',
      description: 'Answer committed to Ethereum Sepolia blockchain',
    },
    escalated: {
      icon: FiAlertCircle,
      label: '🔁 Escalated to Admin',
      color: 'bg-red-100 text-red-800',
      description: 'Low confidence - waiting for human response',
    },
  }

  const config = statusConfig[status] || statusConfig.pending
  const IconComponent = config.icon

  return (
    <>
      <div className={`inline-flex items-center gap-2 px-3 py-2 rounded-full ${config.color} text-xs font-bold cursor-pointer hover:opacity-80 transition`}
        onClick={() => txHash && setShowModal(true)}
        title={config.description}
      >
        <IconComponent size={14} />
        <span>{config.label}</span>
      </div>

      {showModal && txHash && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 max-w-sm w-full">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-bold">Blockchain Verification</h3>
              <button
                onClick={() => setShowModal(false)}
                className="text-gray-500 hover:text-gray-700"
              >
                <FiX size={20} />
              </button>
            </div>
            <p className="text-sm text-gray-600 mb-3">Transaction Hash:</p>
            <code className="block bg-gray-100 p-2 rounded text-xs text-gray-800 overflow-auto mb-4 break-all">
              {txHash}
            </code>
            <a
              href={`https://sepolia.etherscan.io/tx/${txHash}`}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-500 hover:text-blue-700 text-sm font-bold"
            >
              View on Sepolia Etherscan →
            </a>
          </div>
        </div>
      )}
    </>
  )
}

VerificationBadge.propTypes = {
  status: PropTypes.oneOf(['verified', 'pending', 'blockchain', 'escalated']).isRequired,
  txHash: PropTypes.string,
  onViewTx: PropTypes.func,
}
