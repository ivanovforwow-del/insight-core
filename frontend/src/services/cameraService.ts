import apiClient from './api';
import { Camera } from '../types';

const CAMERA_API_ENDPOINT = '/cameras';

export const cameraService = {
  // Get all cameras
 getAllCameras: async (): Promise<Camera[]> => {
    const response = await apiClient.get<Camera[]>(CAMERA_API_ENDPOINT);
    return response.data;
  },

  // Get camera by ID
  getCameraById: async (id: number): Promise<Camera> => {
    const response = await apiClient.get<Camera>(`${CAMERA_API_ENDPOINT}/${id}`);
    return response.data;
  },

  // Create new camera
  createCamera: async (cameraData: Partial<Camera>): Promise<Camera> => {
    const response = await apiClient.post<Camera>(CAMERA_API_ENDPOINT, cameraData);
    return response.data;
  },

  // Update camera
 updateCamera: async (id: number, cameraData: Partial<Camera>): Promise<Camera> => {
    const response = await apiClient.put<Camera>(`${CAMERA_API_ENDPOINT}/${id}`, cameraData);
    return response.data;
  },

  // Delete camera
  deleteCamera: async (id: number): Promise<void> => {
    await apiClient.delete(`${CAMERA_API_ENDPOINT}/${id}`);
  },

  // Update camera status
  updateCameraStatus: async (id: number, enabled: boolean): Promise<Camera> => {
    const response = await apiClient.patch<Camera>(`${CAMERA_API_ENDPOINT}/${id}/status`, {
      enabled,
    });
    return response.data;
  },

  // Get camera stream URL
  getStreamUrl: async (id: number): Promise<string> => {
    const response = await apiClient.get<{ streamUrl: string }>(`${CAMERA_API_ENDPOINT}/${id}/stream`);
    return response.data.streamUrl;
  },
};