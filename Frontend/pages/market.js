import { useEffect, useState } from 'react'

export default function Market() {
  const [prices, setPrices] = useState({})

  useEffect(() => {
    setPrices({
      AAPL: 172.34,
      GOOG: 2845.12,
      TSLA: 695.23
    })
  }, [])

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center px-4">
      <div className="w-full max-w-lg bg-white rounded-lg shadow p-8">
        <h2 className="text-2xl font-bold mb-6 text-gray-800 text-center">Market Prices</h2>
        <ul className="divide-y divide-gray-200">
          {Object.entries(prices).map(([symbol, price]) => (
            <li key={symbol} className="py-2 flex justify-between">
              <span className="font-semibold text-blue-700">{symbol}</span>
              <span className="text-gray-700">${price}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}
