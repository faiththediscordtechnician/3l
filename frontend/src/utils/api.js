const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

let authToken = localStorage.getItem('authToken')

export const setAuthToken = (token) => {
  authToken = token
  localStorage.setItem('authToken', token)
}

export const getAuthToken = () => authToken

export const clearAuthToken = () => {
  authToken = null
  localStorage.removeItem('authToken')
}

const apiCall = async (method, endpoint, data = null, options = {}) => {
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  }

  if (authToken) {
    headers.Authorization = `Bearer ${authToken}`
  }

  const config = {
    method,
    headers,
  }

  if (data) {
    config.body = JSON.stringify(data)
  }

  const response = await fetch(`${API_URL}${endpoint}`, config)

  if (response.status === 401) {
    clearAuthToken()
    window.location.href = '/login'
    throw new Error('Unauthorized')
  }

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || `HTTP ${response.status}`)
  }

  if (response.headers.get('content-type')?.includes('application/json')) {
    return await response.json()
  }

  return response
}

export const auth = {
  register: (username, password) => apiCall('POST', '/auth/register', { username, password }),
  login: (username, password) => apiCall('POST', '/auth/login', { username, password }),
}

export const classes = {
  list: () => apiCall('GET', '/classes/'),
  create: (classData) => apiCall('POST', '/classes/', classData),
  get: (id) => apiCall('GET', `/classes/${id}`),
  update: (id, classData) => apiCall('PUT', `/classes/${id}`, classData),
  delete: (id) => apiCall('DELETE', `/classes/${id}`),
}

export const readings = {
  list: (classId = null) => apiCall('GET', `/readings/?${classId ? `class_id=${classId}` : ''}`),
  create: (readingData) => apiCall('POST', '/readings/', readingData),
  get: (id) => apiCall('GET', `/readings/${id}`),
  update: (id, readingData) => apiCall('PUT', `/readings/${id}`, readingData),
  updateProgress: (id, pagesRead, readingTime) => apiCall('PATCH', `/readings/${id}`, { pages_read: pagesRead, reading_time_minutes: readingTime }),
  delete: (id) => apiCall('DELETE', `/readings/${id}`),
}

export const notes = {
  list: (readingId = null) => apiCall('GET', `/notes/?${readingId ? `reading_id=${readingId}` : ''}`),
  create: (noteData) => apiCall('POST', '/notes/', noteData),
  get: (id) => apiCall('GET', `/notes/${id}`),
  update: (id, noteData) => apiCall('PUT', `/notes/${id}`, noteData),
  delete: (id) => apiCall('DELETE', `/notes/${id}`),
}

export const todos = {
  list: (classId = null, completed = null) => {
    let query = ''
    if (classId) query += `class_id=${classId}&`
    if (completed !== null) query += `completed=${completed}`
    return apiCall('GET', `/todos/?${query}`)
  },
  create: (todoData) => apiCall('POST', '/todos/', todoData),
  get: (id) => apiCall('GET', `/todos/${id}`),
  update: (id, todoData) => apiCall('PUT', `/todos/${id}`, todoData),
  toggle: (id) => apiCall('PATCH', `/todos/${id}/toggle`, {}),
  delete: (id) => apiCall('DELETE', `/todos/${id}`),
}

export const search = {
  canlii: (query) => apiCall('GET', `/search/canlii?query=${encodeURIComponent(query)}`),
  googleScholar: (query) => apiCall('GET', `/search/google-scholar?query=${encodeURIComponent(query)}`),
}

export const annotations = {
  list: (readingId = null) => apiCall('GET', `/annotations/?${readingId ? `reading_id=${readingId}` : ''}`),
  create: (annotationData) => apiCall('POST', '/annotations/', annotationData),
  get: (id) => apiCall('GET', `/annotations/${id}`),
  update: (id, annotationData) => apiCall('PUT', `/annotations/${id}`, annotationData),
  delete: (id) => apiCall('DELETE', `/annotations/${id}`),
}

export const exportData = {
  readingMarkdown: (readingId) => apiCall('GET', `/export/reading/${readingId}/markdown`, null, { headers: {} }),
  readingPdf: (readingId) => apiCall('GET', `/export/reading/${readingId}/pdf`, null, { headers: {} }),
  classMarkdown: (classId) => apiCall('GET', `/export/class/${classId}/markdown`, null, { headers: {} }),
}

export const setup = {
  seedClasses: () => apiCall('POST', '/setup/seed-classes', {}),
  getStatus: () => apiCall('GET', '/setup/status'),
}
