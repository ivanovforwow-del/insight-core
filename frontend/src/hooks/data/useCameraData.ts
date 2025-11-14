import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { cameraService } from '../../services/cameraService';
import { Camera } from '../../types';

// Query keys for camera data
const CAMERA_QUERY_KEYS = {
  all: ['cameras'] as const,
  lists: () => [...CAMERA_QUERY_KEYS.all, 'list'] as const,
  list: (filters?: any) => [...CAMERA_QUERY_KEYS.lists(), filters] as const,
 details: () => [...CAMERA_QUERY_KEYS.all, 'detail'] as const,
  detail: (id: number) => [...CAMERA_QUERY_KEYS.details(), id] as const,
};

export const useCameras = (filters?: any) => {
  return useQuery({
    queryKey: CAMERA_QUERY_KEYS.list(filters),
    queryFn: () => cameraService.getAllCameras(),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

export const useCamera = (id: number) => {
  return useQuery({
    queryKey: CAMERA_QUERY_KEYS.detail(id),
    queryFn: () => cameraService.getCameraById(id),
    enabled: !!id,
  });
};

export const useCreateCamera = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (cameraData: Partial<Camera>) => cameraService.createCamera(cameraData),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: CAMERA_QUERY_KEYS.lists() });
    },
  });
};

export const useUpdateCamera = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<Camera> }) => 
      cameraService.updateCamera(id, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: CAMERA_QUERY_KEYS.detail(id) });
      queryClient.invalidateQueries({ queryKey: CAMERA_QUERY_KEYS.lists() });
    },
  });
};

export const useDeleteCamera = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => cameraService.deleteCamera(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: CAMERA_QUERY_KEYS.lists() });
    },
  });
};

export const useUpdateCameraStatus = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, enabled }: { id: number; enabled: boolean }) => 
      cameraService.updateCameraStatus(id, enabled),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: CAMERA_QUERY_KEYS.detail(id) });
      queryClient.invalidateQueries({ queryKey: CAMERA_QUERY_KEYS.lists() });
    },
  });
};