import Link from 'next/link'

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center px-4">
      <div className="w-full max-w-lg bg-white rounded-lg shadow p-8">
        <h1 className="text-3xl font-bold mb-6 text-center text-blue-700">Market Risk Management Dashboard</h1>
        <nav>
          <ul className="flex flex-col gap-4">
            <li>
              <Link href="/portfolio" className="block bg-blue-600 text-white px-6 py-3 rounded hover:bg-blue-700 text-center transition">Portfolio</Link>
            </li>
            <li>
              <Link href="/market" className="block bg-blue-600 text-white px-6 py-3 rounded hover:bg-blue-700 text-center transition">Market Prices</Link>
            </li>
            <li>
              <Link href="/risk" className="block bg-blue-600 text-white px-6 py-3 rounded hover:bg-blue-700 text-center transition">Risk Metrics</Link>
            </li>
            <li>
              <Link href="/simulate" className="block bg-blue-600 text-white px-6 py-3 rounded hover:bg-blue-700 text-center transition">Simulations</Link>
            </li>
          </ul>
        </nav>
      </div>
    </div>
  )
}
