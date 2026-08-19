import React, { useState, useEffect } from 'react'
import { checkHealth } from './api'
import Overview from './components/Overview'
import Sources from './components/Sources'
import Alerts from './components/Alerts'
import Demo from './components/Demo'

const TABS = ['Overview', 'Sources', 'Alerts', 'Demo']

export default function App() {
  const [activeTab, setActiveTab] = useState('Overview')
  const [isLive, setIsLive] = useState(false)

  useEffect(() => {
    const ping = () => {
      checkHealth()
        .then(() => setIsLive(true))
        .catch(() => setIsLive(false))
    }
    ping()
    const interval = setInterval(ping, 5000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div style={{ minHeight: '100vh', background: '#0a0e14', color: '#e2e8f0' }}>
      <header style={{
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        padding: '16px 32px', borderBottom: '1px solid #1e2530'
      }}>
        <div>
          <h2 style={{ margin: 0 }}>TI-Hunt</h2>
          <span style={{ fontSize: 12, color: '#8892a0' }}>CTI TRIAGE ENGINE</span>
        </div>

        <nav style={{ display: 'flex', gap: 24 }}>
          {TABS.map(tab => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              style={{
                background: 'none', border: 'none', cursor: 'pointer',
                color: activeTab === tab ? '#5b8def' : '#8892a0',
                fontWeight: activeTab === tab ? 600 : 400,
                fontSize: 15
              }}
            >
              {tab}
            </button>
          ))}
        </nav>

        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <span style={{ width: 8, height: 8, borderRadius: '50%', background: isLive ? '#22c55e' : '#ef4444' }} />
          <span style={{ color: isLive ? '#22c55e' : '#ef4444', fontSize: 14 }}>
            {isLive ? 'Live' : 'Offline'}
          </span>
        </div>
      </header>

      <main style={{ padding: 32 }}>
        {activeTab === 'Overview' && <Overview />}
        {activeTab === 'Sources' && <Sources />}
        {activeTab === 'Alerts' && <Alerts />}
        {activeTab === 'Demo' && <Demo />}
      </main>
    </div>
  )
}