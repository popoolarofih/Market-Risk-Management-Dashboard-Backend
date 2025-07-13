import Link from 'next/link'

export default function Home() {
  return (
    <div>
      <h1>Market Risk Management Dashboard</h1>
      <nav>
        <ul>
          <li><Link href="/portfolio">Portfolio</Link></li>
          <li><Link href="/market">Market Prices</Link></li>
          <li><Link href="/risk">Risk Metrics</Link></li>
          <li><Link href="/simulate">Simulations</Link></li>
        </ul>
      </nav>
    </div>
  )
}
