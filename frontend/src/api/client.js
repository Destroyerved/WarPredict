import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_URL || '/api'

const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json'
  }
})

apiClient.interceptors.response.use(
  response => response.data,
  error => {
    const message = error.response?.data?.detail || error.response?.data?.message || error.message || 'API request failed'
    console.error('API Error:', message)
    return Promise.reject(new Error(message))
  }
)

export const predictionApi = {
  predictConflict: (data) => apiClient.post('/predict/conflict', data),
  predictType: (data) => apiClient.post('/predict/type', data)
}

export const simulationApi = {
  runWarSimulation: (data) => apiClient.post('/simulate/war', data),
  getCountries: () => apiClient.get('/simulate/countries'),
  getCountryInfo: (countryId) => apiClient.get(`/simulate/country/${countryId}`)
}

export const countriesApi = {
  getCountries: () => apiClient.get('/countries'),
  getCountry: (code) => apiClient.get(`/countries/${code}`),
  getRiskFactors: (code) => apiClient.get(`/countries/${code}/risk-factors`),
  getHistory: (code) => apiClient.get(`/countries/${code}/history`)
}

export default apiClient