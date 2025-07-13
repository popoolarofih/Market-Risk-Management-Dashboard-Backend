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
      // Replace with your JWT token
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
    <div>
      <h2>Create Portfolio</h2>
      <input placeholder="Portfolio Name" value={name} onChange={e => setName(e.target.value)} />
      <h3>Add Asset</h3>
      <input placeholder="Symbol" value={symbol} onChange={e => setSymbol(e.target.value)} />
      <input placeholder="Quantity" type="number" value={quantity} onChange={e => setQuantity(e.target.value)} />
      <select value={assetType} onChange={e => setAssetType(e.target.value)}>
        <option value="stock">Stock</option>
        <option value="bond">Bond</option>
      </select>
      <button onClick={addAsset}>Add Asset</button>
      <ul>
        {assets.map((a, i) => (
          <li key={i}>{a.symbol} - {a.quantity} ({a.asset_type})</li>
        ))}
      </ul>
      <button onClick={createPortfolio}>Create Portfolio</button>
      <p>{message}</p>
    </div>
  )
}
