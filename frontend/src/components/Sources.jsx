import React, { useEffect, useState } from 'react'
import { fetchSources } from '../api'
import SourceCard from './SourceCard'

export default function Sources() {
  const [sources, setSources] = useState([])

  useEffect(() => {
    const poll = () => fetchSources().then(setSources).catch(() => {})
    poll()
    const interval = setInterval(poll, 4000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div>
      <h3>All Sources</h3>
      <div style={{ display: 'flex', gap: 20, flexWrap: 'wrap' }}>
        {sources.map(s => <SourceCard key={s.id} source={s} />)}
      </div>
    </div>
  )
}