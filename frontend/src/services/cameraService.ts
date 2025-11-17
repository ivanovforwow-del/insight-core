import apiClient from './api';
import { Camera } from '../types';

const CAMERA_API_ENDPOINT = '/cameras';

export const cameraService = {
  // Получить все камеры
 getAllCameras: async (): Promise<Camera[]> => {
    const response = await apiClient.get<Camera[]>(CAMERA_API_ENDPOINT);
    return response.data;
  },

  // Получить камеру по ID
  getCameraById: async (id: number): Promise<Camera> => {
    const response = await apiClient.get<Camera>(`${CAMERA_API_ENDPOINT}/${id}`);
    return response.data;
  },

  // Создать новую камеру
  createCamera: async (cameraData: Partial<Camera>): Promise<Camera> => {
    const response = await apiClient.post<Camera>(CAMERA_API_ENDPOINT, cameraData);
    return response.data;
  },

  // Обновить камеру
 updateCamera: async (id: number, cameraData: Partial<Camera>): Promise<Camera> => {
    const response = await apiClient.put<Camera>(`${CAMERA_API_ENDPOINT}/${id}`, cameraData);
    return response.data;
  },

  // Удалить камеру
  deleteCamera: async (id: number): Promise<void> => {
    await apiClient.delete(`${CAMERA_API_ENDPOINT}/${id}`);
  },

  // Обновить статус камеры
  updateCameraStatus: async (id: number, enabled: boolean): Promise<Camera> => {
    const response = await apiClient.patch<Camera>(`${CAMERA_API_ENDPOINT}/${id}/status`, {
      enabled,
    });
    return response.data;
  },

  // Получить URL потока камеры
  getStreamUrl: async (id: number): Promise<string> => {
    const response = await apiClient.get<{ streamUrl: string }>(`${CAMERA_API_ENDPOINT}/${id}/stream`);
    return response.data.streamUrl;
  },
};