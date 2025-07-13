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
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center px-4">
      <div className="w-full max-w-xl bg-white rounded-lg shadow p-8">
        <h2 className="text-2xl font-bold mb-6 text-gray-800 text-center">Risk Metrics</h2>
        <div className="flex flex-col md:flex-row items-center gap-4 mb-6">
          <input
            className="border border-gray-300 rounded px-4 py-2 w-full md:w-2/3 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Portfolio ID"
            value={portfolioId}
            onChange={e => setPortfolioId(e.target.value)}
          />
          <button
            className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 transition"
            onClick={fetchRisk}
          >
            Fetch Risk
          </button>
        </div>
        {metrics && (
          <div className="bg-gray-100 rounded p-4">
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={[
                { name: 'VaR', value: metrics.VaR },
                { name: 'ES', value: metrics.ES }
              ]}>
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="value" fill="#2563eb" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>
    </div>
  )
}
