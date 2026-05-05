import axios from 'axios';
import { getCustomerToken, logoutCustomer } from '../../auth_token';

export const customerClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:3001',
  timeout: 10000, // 10 seconds
});

customerClient.interceptors.request.use(
  (config) => {
    const token = getCustomerToken();
    if (token) {
      config.headers = config.headers || {};

      config.headers.Authorization = token;
    }

    if (
      config.method === 'post' ||
      config.method === 'put' ||
      config.method === 'patch' ||
      config.method === 'get'
    ) {
      config.headers = config.headers || {};
      if (!config.headers['Content-Type']) {
        config.headers['Content-Type'] = 'application/json';
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor: Handle 401 errors and logout
customerClient.interceptors.response.use(
  (res) => res,
  (err) => {
    // Handle 401 Unauthorized: logout() already clears tokens and redirects
    if (err.response?.status === 401) {
      // 🚫 Không auto logout
      // FE sẽ tự xử lý
      return Promise.reject({
        ...err,
        _authError: true, // gắn cờ cho FE biết là lỗi đăng nhập
      });
    }
    // Handle network errors or other cases
    return Promise.reject(err);
  }
);
