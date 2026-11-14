import axios from 'axios';
import type { InternalAxiosRequestConfig, AxiosError } from 'axios';

// Using localhost instead of 127.0.0.1 to prevent any CORS issues
const API_URL = 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('token');
    if (token) {
      // THIS IS THE CRITICAL LINE. It must use backticks ` and ${token}
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error: AxiosError) => Promise.reject(error)
);

export default apiClient;