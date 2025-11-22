import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle 401 errors (token expired)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const getProducts = async () => {
  const response = await api.get('/products/');
  return response.data;
};

export const createProduct = async (product: any) => {
  const response = await api.post('/products/', product);
  return response.data;
};

export const getWarehouses = async () => {
  const response = await api.get('/warehouses/');
  return response.data;
};

export const createWarehouse = async (warehouse: any) => {
  const response = await api.post('/warehouses/', warehouse);
  return response.data;
};

// Operations API
export const createReceipt = async (receipt: any) => {
  const response = await api.post('/operations/receipts/', receipt);
  return response.data;
};

export const createDelivery = async (delivery: any) => {
  const response = await api.post('/operations/deliveries/', delivery);
  return response.data;
};

export const createTransfer = async (transfer: any) => {
  const response = await api.post('/operations/transfers/', transfer);
  return response.data;
};

export const createAdjustment = async (adjustment: any) => {
  const response = await api.post('/operations/adjustments/', adjustment);
  return response.data;
};

export const getRecentOperations = async () => {
  const response = await api.get('/operations/recent/');
  return response.data;
};

export const updateTransactionStatus = async (transactionId: number, status: string) => {
  const response = await api.patch(`/operations/${transactionId}/status`, { status });
  return response.data;
};

export default api;

