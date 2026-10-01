import axios from 'axios'

const API_BASE = (typeof process !== 'undefined' && process.env?.REACT_APP_API_URL) || 
  (typeof import.meta !== 'undefined' && import.meta.env?.VITE_API_URL) || 
  'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
})

// Add response interceptor for error handling
api.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

export const sendQuery = async (query) => {
  try {
    const response = await api.post('/query', { query })
    return {
      answer: response.data.answer,
      confidence_score: response.data.confidence_score || 0.5,
      trust_score: response.data.trust_score || 0.5,
      sources: response.data.sources || [],
      verification_status: response.data.verification_status || 'pending',
      timestamp: response.data.timestamp || new Date().toISOString(),
    }
  } catch (error) {
    console.error('Error sending query:', error.message)
    return {
      answer: 'Error: Unable to generate answer. Please try again.',
      confidence_score: 0,
      trust_score: 0,
      sources: [],
      verification_status: 'error',
      timestamp: new Date().toISOString(),
    }
  }
}

export const getQueryHistory = async () => {
  try {
    const response = await api.get('/history')
    return response.data || []
  } catch (error) {
    console.error('Error fetching history:', error.message)
    return []
  }
}

export const submitFeedback = async (queryId, rating, comment) => {
  try {
    const response = await api.post('/feedback', {
      query_id: queryId,
      rating,
      comment,
    })
    return response.data
  } catch (error) {
    console.error('Error submitting feedback:', error.message)
    return { success: false }
  }
}

export const checkBlockchainStatus = async (txHash) => {
  try {
    const response = await api.get(`/blockchain/${txHash}`)
    return response.data
  } catch (error) {
    console.error('Error checking blockchain status:', error.message)
    return { verified: false }
  }
}

export default api
