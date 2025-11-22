import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
});

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

