import React, { useEffect, useState, useRef } from 'react'
import { fetchSources, fetchAlerts } from '../api'
import SourceCard from './SourceCard'
import TrustChart from './TrustChart'

export default function Overview() {
  const [sources, setSources] = useState([])
  const [alerts, setAlerts] = useState([])
  const [history, setHistory] = useState([])
  const tickRef = useRef(0)

  useEffect(() => {
    const poll = () => {
      fetchSources().then(data => {
        setSources(data)
        tickRef.current += 1
        setHistory(prev => {
          const point = { tick: tickRef.current }
          data.forEach(s => { point[s.name] = +(s.trust_score * 100).toFixed(1) })
          const next = [...prev, point]
          return next.slice(-30) // keep last 30 points
        })
      }).catch(() => {})
      fetchAlerts().then(setAlerts).catch(() => {})
    }
    poll()
    const interval = setInterval(poll, 4000)
    return () => clearInterval(interval)
  }, [])

  const activeCount = sources.length
  const aboveThreshold = sources.filter(s => s.trust_score >= 0.6).length
  const avgTrust = sources.length
    ? (sources.reduce((sum, s) => sum + s.trust_score, 0) / sources.length * 100).toFixed(1)
    : null
  const forwardedCount = alerts.filter(a => a.forwarded_to_siem).length
  const throttledCount = sources.filter(s => s.is_throttled).length

  const cardStyle = {
    background: '#0f1420', border: '1px solid #1e2530', borderRadius: 12,
    padding: 20, flex: 1
  }

  return (
    <div>
      <div style={{ display: 'flex', gap: 20, marginBottom: 24 }}>
        <div style={cardStyle}>
          <div style={{ color: '#8892a0', fontSize: 13 }}>Active Sources</div>
          <div style={{ fontSize: 32, fontWeight: 700 }}>{activeCount}</div>
          <div style={{ color: '#8892a0', fontSize: 12 }}>{aboveThreshold} above SIEM threshold</div>
        </div>
        <div style={cardStyle}>
          <div style={{ color: '#8892a0', fontSize: 13 }}>Avg Trust Score</div>
          <div style={{ fontSize: 32, fontWeight: 700 }}>{avgTrust ? `${avgTrust}%` : '—%'}</div>
          <div style={{ color: '#8892a0', fontSize: 12 }}>across all sources</div>
        </div>
        <div style={cardStyle}>
          <div style={{ color: '#8892a0', fontSize: 13 }}>Alerts Forwarded</div>
          <div style={{ fontSize: 32, fontWeight: 700 }}>{forwardedCount}</div>
          <div style={{ color: '#8892a0', fontSize: 12 }}>to SIEM this session</div>
        </div>
        <div style={cardStyle}>
          <div style={{ color: '#8892a0', fontSize: 13 }}>Throttled Sources</div>
          <div style={{ fontSize: 32, fontWeight: 700 }}>{throttledCount}</div>
          <div style={{ color: '#8892a0', fontSize: 12 }}>
            {throttledCount > 0 ? 'circuit breaker active' : 'all sources healthy'}
          </div>
        </div>
      </div>

      <div style={{ background: '#0f1420', border: '1px solid #1e2530', borderRadius: 12, padding: 20, marginBottom: 24 }}>
        <h3 style={{ marginTop: 0 }}>Live Trust Score History <span style={{ fontSize: 13, color: '#8892a0', fontWeight: 400 }}>— EXP3 probability over time</span></h3>
        <TrustChart history={history} sourceNames={sources.map(s => s.name)} />
      </div>

      <h3>Source Trust Cards</h3>
      {sources.length === 0 ? (
        <div style={{ color: '#8892a0' }}>No sources registered yet — inject an event via the Demo tab.</div>
      ) : (
        <div style={{ display: 'flex', gap: 20, flexWrap: 'wrap' }}>
          {sources.map(s => <SourceCard key={s.id} source={s} />)}
        </div>
      )}
    </div>
  )
}