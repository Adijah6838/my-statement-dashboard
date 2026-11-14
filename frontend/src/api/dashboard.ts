import apiClient from './client';

export interface Statement {
  id: number;
  transaction_type: string;
  description: string;
  amount: number;
  date: string;
  sender_name?: string;
  receiver_name?: string;
  status: string;
}

export interface PaginatedStatements {
  items: Statement[];
  total: number;
  skip: number;
  limit: number;
}

export interface BalanceResponse {
  balance: number;
  full_name: string;
}

export const getBalance = async (): Promise<BalanceResponse> => {
  const response = await apiClient.get('/statements/balance');
  return response.data;
};

export const getStatements = async (skip: number = 0, limit: number = 5): Promise<PaginatedStatements> => {
  const response = await apiClient.get(`/statements/?skip=${skip}&limit=${limit}`);
  return response.data;
};