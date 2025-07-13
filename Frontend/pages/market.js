import { useEffect, useState } from 'react'

export default function Market() {
  const [prices, setPrices] = useState({})

  useEffect(() => {
    // Replace with real API call for live prices
    setPrices({
      AAPL: 172.34,
      GOOG: 2845.12,
      TSLA: 695.23
    })
  }, [])

  return (
    <div>
      <h2>Market Prices</h2>
      <ul>
        {Object.entries(prices).map(([symbol, price]) => (
          <li key={symbol}>{symbol}: ${price}</li>
        ))}
      </ul>
    </div>
  )
}
