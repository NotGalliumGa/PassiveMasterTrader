"use client";

import { useEffect, useState } from "react";
import axios from "axios";

interface Trade {
  time: string;
  action: string;
  price: number;
  quantity: number;
}

interface Portfolio {
  cash: number;
  position: number;
  avg_price: number;
  trade_history: Trade[];
}

export default function Home() {
  const [portfolio, setPortfolio] = useState<Portfolio | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    try {
      const res = await axios.get(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/portfolio`
      );
      setPortfolio(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const pauseBot = async () => {
    await axios.post(`${process.env.NEXT_PUBLIC_BACKEND_URL}/pause`);
    fetchData();
  };

  const resumeBot = async () => {
    await axios.post(`${process.env.NEXT_PUBLIC_BACKEND_URL}/resume`);
    fetchData();
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000); // Refresh every 5 sec
    return () => clearInterval(interval);
  }, []);

  if (loading) return <p className="p-4">Loading...</p>;

  return (
    <main className="p-8 max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Trading Bot Dashboard</h1>
      <div className="mb-4">
        <p><strong>Cash:</strong> ${portfolio?.cash.toFixed(2)}</p>
        <p><strong>Position:</strong> {portfolio?.position} shares</p>
        <p><strong>Average Price:</strong> ${portfolio?.avg_price.toFixed(2)}</p>
      </div>

      <div className="flex gap-4 mb-6">
        <button
          onClick={pauseBot}
          className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
        >
          Pause Bot
        </button>
        <button
          onClick={resumeBot}
          className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
        >
          Resume Bot
        </button>
      </div>

      <h2 className="text-xl font-semibold mb-2">Recent Trades</h2>
      <table className="w-full border-collapse">
        <thead>
          <tr className="bg-gray-100">
            <th className="border px-2 py-1">Time</th>
            <th className="border px-2 py-1">Action</th>
            <th className="border px-2 py-1">Price</th>
            <th className="border px-2 py-1">Quantity</th>
          </tr>
        </thead>
        <tbody>
          {portfolio?.trade_history.map((trade, idx) => (
            <tr key={idx}>
              <td className="border px-2 py-1">{trade.time}</td>
              <td className="border px-2 py-1">{trade.action}</td>
              <td className="border px-2 py-1">${trade.price.toFixed(2)}</td>
              <td className="border px-2 py-1">{trade.quantity}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}
