import { useState } from 'react'
import axios from 'axios'

export default function Portfolio() {
  const [name, setName] = useState('')
  const [assets, setAssets] = useState([])
  const [symbol, setSymbol] = useState('')
  const [quantity, setQuantity] = useState('')
  const [assetType, setAssetType] = useState('stock')
  const [message, setMessage] = useState('')

  const addAsset = () => {
    setAssets([...assets, { symbol, quantity: Number(quantity), asset_type: assetType }])
    setSymbol('')
    setQuantity('')
    setAssetType('stock')
  }

  const createPortfolio = async () => {
    try {
      const token = localStorage.getItem('token')
      await axios.post('http://127.0.0.1:8000/portfolio', {
        name,
        assets
      }, {
        headers: { Authorization: `Bearer ${token}` }
      })
      setMessage('Portfolio created!')
      setName('')
      setAssets([])
    } catch (err) {
      setMessage('Error creating portfolio')
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center px-4">
      <div className="w-full max-w-xl bg-white rounded-lg shadow p-8">
        <h2 className="text-2xl font-bold mb-6 text-gray-800 text-center">Create Portfolio</h2>
        <input
          className="border border-gray-300 rounded px-4 py-2 w-full mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Portfolio Name"
          value={name}
          onChange={e => setName(e.target.value)}
        />
        <div className="mb-4">
          <h3 className="font-semibold mb-2">Add Asset</h3>
          <div className="flex flex-col md:flex-row gap-2">
            <input
              className="border border-gray-300 rounded px-4 py-2 flex-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Symbol"
              value={symbol}
              onChange={e => setSymbol(e.target.value)}
            />
            <input
              className="border border-gray-300 rounded px-4 py-2 flex-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Quantity"
              type="number"
              value={quantity}
              onChange={e => setQuantity(e.target.value)}
            />
            <select
              className="border border-gray-300 rounded px-4 py-2 flex-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={assetType}
              onChange={e => setAssetType(e.target.value)}
            >
              <option value="stock">Stock</option>
              <option value="bond">Bond</option>
            </select>
            <button
              className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
              onClick={addAsset}
            >
              Add Asset
            </button>
          </div>
        </div>
        <ul className="mb-4">
          {assets.map((a, i) => (
            <li key={i} className="text-gray-700">{a.symbol} - {a.quantity} ({a.asset_type})</li>
          ))}
        </ul>
        <button
          className="bg-green-600 text-white px-6 py-2 rounded hover:bg-green-700 transition w-full"
          onClick={createPortfolio}
        >
          Create Portfolio
        </button>
        <p className="mt-4 text-center text-red-600">{message}</p>
      </div>
    </div>
  )
}
