import apiClient from './api';
import { Event } from '../types';

const EVENT_API_ENDPOINT = '/events';

export const eventService = {
  // Получить все события
  getEvents: async (params?: {
    page?: number;
    limit?: number;
    startDate?: string;
    endDate?: string;
    cameraId?: number;
    objectType?: string;
    severity?: string;
    search?: string;
  }): Promise<{ data: Event[]; total: number; page: number; limit: number }> => {
    const response = await apiClient.get<{ data: Event[]; total: number; page: number; limit: number }>(EVENT_API_ENDPOINT, { params });
    return response.data;
  },

  // Получить событие по ID
  getEventById: async (id: number): Promise<Event> => {
    const response = await apiClient.get<Event>(`${EVENT_API_ENDPOINT}/${id}`);
    return response.data;
  },

  // Получить последние события
  getRecentEvents: async (limit: number = 10): Promise<Event[]> => {
    const response = await apiClient.get<Event[]>(`${EVENT_API_ENDPOINT}/recent`, { 
      params: { limit } 
    });
    return response.data;
  },

  // Получить события по камере
  getEventsByCamera: async (cameraId: number, params?: {
    page?: number;
    limit?: number;
    startDate?: string;
    endDate?: string;
    objectType?: string;
    severity?: string;
  }): Promise<{ data: Event[]; total: number; page: number; limit: number }> => {
    const response = await apiClient.get<{ data: Event[]; total: number; page: number; limit: number }>(
      `${EVENT_API_ENDPOINT}/camera/${cameraId}`, 
      { params }
    );
    return response.data;
  },

  // Получить статистику событий
  getEventsStats: async (params?: {
    startDate?: string;
    endDate?: string;
    cameraId?: number;
 }): Promise<{
    total: number;
    byType: { type: string; count: number }[];
    byHour: { hour: string; count: number }[];
    byDay: { date: string; count: number }[];
  }> => {
    const response = await apiClient.get<{
      total: number;
      byType: { type: string; count: number }[];
      byHour: { hour: string; count: number }[];
      byDay: { date: string; count: number }[];
    }>(`${EVENT_API_ENDPOINT}/stats`, { params });
    return response.data;
  },

  // Обновить статус события
  updateEventStatus: async (id: number, resolved: boolean): Promise<Event> => {
    const response = await apiClient.patch<Event>(`${EVENT_API_ENDPOINT}/${id}/status`, {
      resolved,
    });
    return response.data;
  },

  // Удалить событие
  deleteEvent: async (id: number): Promise<void> => {
    await apiClient.delete(`${EVENT_API_ENDPOINT}/${id}`);
  },
};