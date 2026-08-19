import React from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ReferenceLine, ResponsiveContainer } from 'recharts'

const COLORS = ['#5b8def', '#22c55e', '#f59e0b', '#a78bfa', '#ec4899']

export default function TrustChart({ history, sourceNames }) {
  if (!history || history.length === 0) {
    return <div style={{ color: '#8892a0', textAlign: 'center', padding: 60 }}>Collecting history...</div>
  }

  return (
    <ResponsiveContainer width="100%" height={350}>
      <LineChart data={history}>
        <CartesianGrid strokeDasharray="3 3" stroke="#1e2530" />
        <XAxis dataKey="tick" stroke="#8892a0" />
        <YAxis domain={[0, 100]} stroke="#8892a0" />
        <Tooltip contentStyle={{ background: '#0f1420', border: '1px solid #1e2530' }} />
        <Legend />
        <ReferenceLine y={60} stroke="#ef4444" strokeDasharray="4 4" label="SIEM threshold" />
        {sourceNames.map((name, i) => (
          <Line
            key={name}
            type="monotone"
            dataKey={name}
            stroke={COLORS[i % COLORS.length]}
            dot={false}
            strokeWidth={2}
          />
        ))}
      </LineChart>
    </ResponsiveContainer>
  )
}