import axios from 'axios';
import { getStaffToken, logoutStaff } from '../../auth_token';

export const staffClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:3001',
  timeout: 10000,
});

// Request interceptor
staffClient.interceptors.request.use(
  (config) => {
    const token = getStaffToken();
    if (token) {
      config.headers = config.headers || {};
      config.headers.Authorization = token;
    }

    if (['post', 'put', 'patch'].includes(config.method || '')) {
      config.headers = config.headers || {};
      if (!config.headers['Content-Type']) {
        config.headers['Content-Type'] = 'application/json';
      }
    }

    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
staffClient.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      // 🚫 Không auto logout
      // FE sẽ tự xử lý
      return Promise.reject({
        ...err,
        _authError: true, // gắn cờ cho FE biết là lỗi đăng nhập
      });
    }
    return Promise.reject(err);
  }
);
