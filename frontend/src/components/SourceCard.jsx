import React from 'react'

export default function SourceCard({ source }) {
  const pct = (source.trust_score * 100).toFixed(1)
  const level = source.trust_score >= 0.6 ? 'HIGH' : 'LOW'

  return (
    <div style={{
      background: '#0f1420', border: `1px solid ${source.is_throttled ? '#ef4444' : '#1e2530'}`,
      borderRadius: 12, padding: 20, minWidth: 220, position: 'relative'
    }}>
      {source.is_throttled && (
        <span style={{
          position: 'absolute', top: 12, right: 12, background: '#3b1416',
          color: '#ef4444', fontSize: 11, padding: '2px 8px', borderRadius: 6
        }}>
          ⚡ THROTTLED
        </span>
      )}
      <h4 style={{ margin: '0 0 8px 0' }}>{source.name}</h4>
      <span style={{
        display: 'inline-block', fontSize: 11, padding: '2px 8px', borderRadius: 6,
        background: level === 'HIGH' ? '#0f2e1f' : '#3b1416',
        color: level === 'HIGH' ? '#22c55e' : '#ef4444'
      }}>
        {level}
      </span>
      <div style={{ fontSize: 32, fontWeight: 700, color: level === 'HIGH' ? '#22c55e' : '#ef4444', marginTop: 8 }}>
        {pct}<span style={{ fontSize: 16 }}>%</span>
      </div>
      <div style={{ fontSize: 12, color: '#8892a0' }}>trust score</div>
    </div>
  )
}