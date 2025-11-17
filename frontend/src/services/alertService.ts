import apiClient from './api';
import { Alert } from '../types';

const ALERT_API_ENDPOINT = '/alerts';

export const alertService = {
  // Получить все оповещения
  getAlerts: async (params?: {
    page?: number;
    limit?: number;
    startDate?: string;
    endDate?: string;
    type?: string;
    read?: boolean;
    search?: string;
  }): Promise<{ data: Alert[]; total: number; page: number; limit: number }> => {
    const response = await apiClient.get<{ data: Alert[]; total: number; page: number; limit: number }>(ALERT_API_ENDPOINT, { params });
    return response.data;
  },

  // Получить оповещение по ID
  getAlertById: async (id: number): Promise<Alert> => {
    const response = await apiClient.get<Alert>(`${ALERT_API_ENDPOINT}/${id}`);
    return response.data;
  },

  // Получить количество непрочитанных оповещений
  getUnreadAlertsCount: async (): Promise<number> => {
    const response = await apiClient.get<{ count: number }>(`${ALERT_API_ENDPOINT}/unread`);
    return response.data.count;
  },

  // Получить последние оповещения
  getRecentAlerts: async (limit: number = 10): Promise<Alert[]> => {
    const response = await apiClient.get<Alert[]>(`${ALERT_API_ENDPOINT}/recent`, { 
      params: { limit } 
    });
    return response.data;
  },

  // Отметить оповещение как прочитанное
 markAlertAsRead: async (id: number): Promise<Alert> => {
    const response = await apiClient.patch<Alert>(`${ALERT_API_ENDPOINT}/${id}/read`);
    return response.data;
  },

  // Отметить все оповещения как прочитанные
  markAllAlertsAsRead: async (): Promise<void> => {
    await apiClient.patch(`${ALERT_API_ENDPOINT}/read-all`);
  },

  // Удалить оповещение
  deleteAlert: async (id: number): Promise<void> => {
    await apiClient.delete(`${ALERT_API_ENDPOINT}/${id}`);
  },

  // Удалить все оповещения
  deleteAllAlerts: async (): Promise<void> => {
    await apiClient.delete(`${ALERT_API_ENDPOINT}/all`);
  },
};