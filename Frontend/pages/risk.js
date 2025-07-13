import { useState } from 'react'
import axios from 'axios'
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts'

export default function Risk() {
  const [portfolioId, setPortfolioId] = useState('')
  const [metrics, setMetrics] = useState(null)

  const fetchRisk = async () => {
    const token = localStorage.getItem('token')
    const res = await axios.get(`http://127.0.0.1:8000/portfolio/${portfolioId}/risk`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    setMetrics(res.data)
  }

  return (
    <div>
      <h2>Risk Metrics</h2>
      <input placeholder="Portfolio ID" value={portfolioId} onChange={e => setPortfolioId(e.target.value)} />
      <button onClick={fetchRisk}>Fetch Risk</button>
      {metrics && (
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={[
            { name: 'VaR', value: metrics.VaR },
            { name: 'ES', value: metrics.ES }
          ]}>
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="value" fill="#8884d8" />
          </BarChart>
        </ResponsiveContainer>
      )}
    </div>
  )
}
