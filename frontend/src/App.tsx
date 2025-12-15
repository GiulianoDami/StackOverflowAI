
import React, { useState, useEffect } from 'react'
import axios from 'axios'

interface AIResponse {
  answer: string
  sources: number[]
}

const App: React.FC = () => {
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const [response, setResponse] = useState<AIResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResponse(null)

    try {
      const res = await axios.post<AIResponse>('http://localhost:8000/api/ask', {
        query,
        top_k: 5
      })
      setResponse(res.data)
    } catch (err: any) {
      setError(err.message || 'Error occurred')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ maxWidth: 600, margin: '2rem auto', fontFamily: 'Arial, sans-serif' }}>
      <h1>StackOverflowAI Chat</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Ask a programming question..."
          value={query}
          onChange={e => setQuery(e.target.value)}
          style={{ width: "100%", padding: 8, fontSize: 16 }}
          required
        />
        <button type="submit" disabled={loading} style={{ marginTop: 10, padding: '8px 16px' }}>
          {loading ? 'Thinking...' : 'Ask'}
        </button>
      </form>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {response && (
        <>
          <h3>Answer:</h3>
          <p>{response.answer}</p>
          <h4>Sources:</h4>
          <ul>
            {response.sources.map(id => (
              <li key={id}>Q&A ID: {id}</li>
            ))}
          </ul>
        </>
      )}
    </div>
  )
}

export default App
```

```plaintext
