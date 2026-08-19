import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000'
})

export const fetchSources = () =>
  api.get('/api/v1/sources').then(r => r.data)

export const fetchAlerts = () =>
  api.get('/api/v1/alerts').then(r => r.data)

export const injectAlert = (payload) =>
  api.post('/api/v1/alerts', payload).then(r => r.data)

export const submitFeedback = (alertId, verdict) =>
  api.post('/api/v1/feedback', { alert_id: alertId, verdict }).then(r => r.data)

export const checkHealth = () =>
  api.get('/health').then(r => r.data)

export default api