import { useState } from 'react'
import axios from 'axios'

export default function Simulate() {
  const [portfolioId, setPortfolioId] = useState('')
  const [result, setResult] = useState(null)

  const runSimulation = async () => {
    const token = localStorage.getItem('token')
    const res = await axios.get(`http://127.0.0.1:8000/portfolio/${portfolioId}/simulate`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    setResult(res.data)
  }

  return (
    <div>
      <h2>Run Simulation</h2>
      <input placeholder="Portfolio ID" value={portfolioId} onChange={e => setPortfolioId(e.target.value)} />
      <button onClick={runSimulation}>Run Simulation</button>
      {result && (
        <div>
          <h3>Scenario: {result.scenario}</h3>
          <pre>{JSON.stringify(result.result, null, 2)}</pre>
        </div>
      )}
    </div>
  )
}
