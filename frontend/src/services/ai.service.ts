/**
 * AI Service - Connects Vue frontend to Python Agno backend
 */

// In production (same domain), use empty string for relative URLs
// In development, use localhost:8000
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || ''

// Store session ID in sessionStorage for conversation continuity
const SESSION_STORAGE_KEY = 'portfolio_chat_session'

let sessionId: string | null = sessionStorage.getItem(SESSION_STORAGE_KEY)

export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

export interface ChatRequest {
  message: string
  session_id?: string | null
}

export interface ChatResponse {
  response: string
  session_id: string
}

/**
 * Send a message to the AI agent and get a response
 */
export async function chatWithAI(message: string): Promise<string> {
  try {
    const response = await fetch(`${BACKEND_URL}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        session_id: sessionId
      } as ChatRequest)
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }))
      throw new Error(error.detail || `HTTP error ${response.status}`)
    }

    const data: ChatResponse = await response.json()

    // Store session ID for conversation continuity
    sessionId = data.session_id
    sessionStorage.setItem(SESSION_STORAGE_KEY, sessionId)

    return data.response

  } catch (error) {
    console.error('AI chat error:', error)

    if (error instanceof TypeError && error.message.includes('fetch')) {
      return 'Sorry, I couldn\'t connect to the AI backend. Make sure the backend server is running on port 8000.'
    }

    return `Sorry, I had trouble processing that. ${error instanceof Error ? error.message : 'Please try again.'}`
  }
}

/**
 * Check if the backend is healthy and ready
 */
export async function checkBackendHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${BACKEND_URL}/api/health`)
    const data = await response.json()
    return data.status === 'healthy'
  } catch (error) {
    console.error('Backend health check failed:', error)
    return false
  }
}

/**
 * Reset the conversation session (clear memory)
 */
export function resetSession(): void {
  sessionId = null
  sessionStorage.removeItem(SESSION_STORAGE_KEY)
}

/**
 * Get current session ID
 */
export function getSessionId(): string | null {
  return sessionId
}
