// Base API URL
const API_BASE_URL = 'http://localhost:8000/api';

// Helper function to get auth token
function getAuthToken() {
  return localStorage.getItem('authToken');
}

// Generic API call function with authentication
async function apiCall(endpoint, method = 'GET', data = null) {
  const url = `${API_BASE_URL}${endpoint}`;
  const token = getAuthToken();
  
  const headers = {
    'Content-Type': 'application/json'
  };
  
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  
  const options = {
    method,
    headers,
    credentials: 'include'
  };
  
  if (data && (method === 'POST' || method === 'PUT')) {
    options.body = JSON.stringify(data);
  }
  
  try {
    const response = await fetch(url, options);
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'API call failed');
    }
    
    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
}

// Driver API functions
const DriversAPI = {
  getAll: () => apiCall('/drivers'),
  getById: (id) => apiCall(`/drivers/${id}`),
  create: (driverData) => apiCall('/drivers', 'POST', driverData),
  update: (id, driverData) => apiCall(`/drivers/${id}`, 'PUT', driverData),
  delete: (id) => apiCall(`/drivers/${id}`, 'DELETE'),
  query: (queryParams) => apiCall('/queries/drivers', 'POST', queryParams),
  compare: (id1, id2) => apiCall('/queries/compare-drivers', 'POST', { id1, id2 })
};

// Team API functions
const TeamsAPI = {
  getAll: () => apiCall('/teams'),
  getById: (id) => apiCall(`/teams/${id}`),
  create: (teamData) => apiCall('/teams', 'POST', teamData),
  update: (id, teamData) => apiCall(`/teams/${id}`, 'PUT', teamData),
  delete: (id) => apiCall(`/teams/${id}`, 'DELETE'),
  query: (queryParams) => apiCall('/queries/teams', 'POST', queryParams),
  compare: (id1, id2) => apiCall('/queries/compare-teams', 'POST', { id1, id2 })
};