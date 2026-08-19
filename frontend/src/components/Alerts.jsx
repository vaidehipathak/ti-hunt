import React, { useEffect, useState } from 'react'
import { fetchAlerts } from '../api'

export default function Alerts() {
  const [alerts, setAlerts] = useState([])

  useEffect(() => {
    const poll = () => fetchAlerts().then(setAlerts).catch(() => {})
    poll()
    const interval = setInterval(poll, 4000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div>
      <h3>Recent Alerts</h3>
      {alerts.length === 0 ? (
        <div style={{ color: '#8892a0' }}>No alerts yet — inject some events via the Demo tab.</div>
      ) : (
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ textAlign: 'left', color: '#8892a0', fontSize: 13 }}>
              <th style={{ padding: 8 }}>IOC Type</th>
              <th style={{ padding: 8 }}>Value</th>
              <th style={{ padding: 8 }}>Verdict</th>
              <th style={{ padding: 8 }}>Forwarded to SIEM</th>
            </tr>
          </thead>
          <tbody>
            {alerts.map(a => (
              <tr key={a.id} style={{ borderTop: '1px solid #1e2530' }}>
                <td style={{ padding: 8 }}>{a.ioc_type}</td>
                <td style={{ padding: 8 }}>{a.ioc_value}</td>
                <td style={{ padding: 8 }}>{a.verdict || '—'}</td>
                <td style={{ padding: 8 }}>
                  {a.forwarded_to_siem
                    ? <span style={{ color: '#22c55e' }}>✅ Forwarded</span>
                    : <span style={{ color: '#ef4444' }}>❌ Not forwarded</span>}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}