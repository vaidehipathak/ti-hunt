import React, { useState } from 'react'
import { injectAlert, submitFeedback } from '../api'

const IOC_TYPES = ['ip', 'domain', 'hash', 'url']
const SOURCE_NAMES = ['ThreatFox', 'URLHaus', 'CERT-In', 'Dark Web Feed']

function randomIOC(type) {
  if (type === 'ip') return `${Math.floor(Math.random()*255)}.${Math.floor(Math.random()*255)}.${Math.floor(Math.random()*255)}.${Math.floor(Math.random()*255)}`
  if (type === 'domain') return `evil-${Math.floor(Math.random()*9999)}.example`
  if (type === 'hash') return Math.random().toString(36).substring(2, 15)
  return `http://bad-${Math.floor(Math.random()*9999)}.test/payload`
}

export default function Demo() {
  const [iocType, setIocType] = useState('ip')
  const [iocValue, setIocValue] = useState('')
  const [sourceName, setSourceName] = useState('ThreatFox')
  const [mitreTtp, setMitreTtp] = useState('T1071.001')
  const [lastAlertId, setLastAlertId] = useState('')
  const [alertIdInput, setAlertIdInput] = useState('')
  const [status, setStatus] = useState('')

  const handleRandom = () => {
    const type = IOC_TYPES[Math.floor(Math.random() * IOC_TYPES.length)]
    setIocType(type)
    setIocValue(randomIOC(type))
  }

  const handleInject = async () => {
    try {
      const res = await injectAlert({
        source_name: sourceName,
        ioc_type: iocType,
        ioc_value: iocValue || randomIOC(iocType),
        mitre_ttp: mitreTtp
      })
      setLastAlertId(res.id)
      setAlertIdInput(res.id)
      setStatus(`Injected alert #${res.id} — forwarded: ${res.forwarded_to_siem}`)
    } catch (e) {
      setStatus('Error injecting event — check backend is running')
    }
  }

  const handleVerdict = async (verdict) => {
    if (!alertIdInput) {
      setStatus('Enter an alert ID first')
      return
    }
    try {
      const res = await submitFeedback(Number(alertIdInput), verdict)
      setStatus(`Feedback submitted — new trust score: ${(res.source_trust_score * 100).toFixed(1)}%`)
    } catch (e) {
      setStatus('Error submitting feedback')
    }
  }

  const inputStyle = {
    width: '100%', padding: 10, borderRadius: 8, background: '#0a0e14',
    border: '1px solid #1e2530', color: '#e2e8f0', marginTop: 4
  }

  return (
    <div style={{ display: 'flex', gap: 24 }}>
      <div style={{ flex: 1, background: '#0f1420', border: '1px solid #1e2530', borderRadius: 12, padding: 20 }}>
        <h3 style={{ marginTop: 0 }}>🧪 Inject IOC Event</h3>

        <label style={{ fontSize: 12, color: '#8892a0' }}>IOC TYPE</label>
        <select style={inputStyle} value={iocType} onChange={e => setIocType(e.target.value)}>
          {IOC_TYPES.map(t => <option key={t} value={t}>{t}</option>)}
        </select>

        <label style={{ fontSize: 12, color: '#8892a0', marginTop: 12, display: 'block' }}>IOC VALUE</label>
        <input style={inputStyle} value={iocValue} onChange={e => setIocValue(e.target.value)} placeholder="e.g. 1.2.3.4" />

        <label style={{ fontSize: 12, color: '#8892a0', marginTop: 12, display: 'block' }}>SOURCE NAME</label>
        <select style={inputStyle} value={sourceName} onChange={e => setSourceName(e.target.value)}>
          {SOURCE_NAMES.map(s => <option key={s} value={s}>{s}</option>)}
        </select>

        <label style={{ fontSize: 12, color: '#8892a0', marginTop: 12, display: 'block' }}>MITRE TTP</label>
        <input style={inputStyle} value={mitreTtp} onChange={e => setMitreTtp(e.target.value)} />

        <div style={{ display: 'flex', gap: 12, marginTop: 16 }}>
          <button onClick={handleRandom} style={{ flex: 1, padding: 10, borderRadius: 8, background: '#1e2530', color: '#e2e8f0', border: 'none', cursor: 'pointer' }}>
            🎲 Random
          </button>
          <button onClick={handleInject} style={{ flex: 2, padding: 10, borderRadius: 8, background: '#5b8def', color: 'white', border: 'none', cursor: 'pointer' }}>
            🚀 Inject Event
          </button>
        </div>
      </div>

      <div style={{ flex: 1, background: '#0f1420', border: '1px solid #1e2530', borderRadius: 12, padding: 20 }}>
        <h3 style={{ marginTop: 0 }}>👍 Submit Analyst Verdict</h3>

        <label style={{ fontSize: 12, color: '#8892a0' }}>ALERT ID</label>
        <input
          style={inputStyle}
          value={alertIdInput}
          onChange={e => setAlertIdInput(e.target.value)}
          placeholder="Paste alert_id from inject result above"
        />

        <div style={{ display: 'flex', gap: 12, marginTop: 16 }}>
          <button onClick={() => handleVerdict('true_positive')} style={{ flex: 1, padding: 10, borderRadius: 8, background: '#166534', color: 'white', border: 'none', cursor: 'pointer' }}>
            👍 True Positive
          </button>
          <button onClick={() => handleVerdict('false_positive')} style={{ flex: 1, padding: 10, borderRadius: 8, background: '#3b1416', color: '#ef4444', border: '1px solid #ef4444', cursor: 'pointer' }}>
            👎 False Positive
          </button>
        </div>

        {status && <div style={{ marginTop: 16, fontSize: 13, color: '#8892a0' }}>{status}</div>}

        <div style={{ marginTop: 24, fontSize: 13, color: '#8892a0' }}>
          <strong style={{ color: '#e2e8f0' }}>How it works:</strong> Submitting True Positive increases the source's EXP3 weight.
          Submitting False Positive gives no reward — the source is naturally starved as peers accumulate weight.
          The CUSUM watchdog monitors for sustained probability drops.
        </div>
      </div>
    </div>
  )
}