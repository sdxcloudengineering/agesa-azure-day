import axios from 'axios'

// Relative base: works locally via Vite's dev proxy, and in production via the
// nginx reverse proxy inside the frontend container (see nginx.conf.template).
const apiClient = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

export default apiClient
