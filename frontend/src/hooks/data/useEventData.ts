import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { eventService } from '../../services/eventService';
import { Event } from '../../types';

// Query keys for event data
const EVENT_QUERY_KEYS = {
  all: ['events'] as const,
  lists: () => [...EVENT_QUERY_KEYS.all, 'list'] as const,
  list: (params?: any) => [...EVENT_QUERY_KEYS.lists(), params] as const,
  details: () => [...EVENT_QUERY_KEYS.all, 'detail'] as const,
  detail: (id: number) => [...EVENT_QUERY_KEYS.details(), id] as const,
  recent: (limit?: number) => [...EVENT_QUERY_KEYS.all, 'recent', limit] as const,
  byCamera: (cameraId: number, params?: any) => [...EVENT_QUERY_KEYS.all, 'byCamera', cameraId, params] as const,
 stats: (params?: any) => [...EVENT_QUERY_KEYS.all, 'stats', params] as const,
};

export const useEvents = (params?: {
  page?: number;
  limit?: number;
  startDate?: string;
  endDate?: string;
  cameraId?: number;
  objectType?: string;
  severity?: string;
  search?: string;
}) => {
  return useQuery({
    queryKey: EVENT_QUERY_KEYS.list(params),
    queryFn: () => eventService.getEvents(params),
    staleTime: 30 * 1000, // 30 seconds
  });
};

export const useEvent = (id: number) => {
  return useQuery({
    queryKey: EVENT_QUERY_KEYS.detail(id),
    queryFn: () => eventService.getEventById(id),
    enabled: !!id,
  });
};

export const useRecentEvents = (limit: number = 10) => {
  return useQuery({
    queryKey: EVENT_QUERY_KEYS.recent(limit),
    queryFn: () => eventService.getRecentEvents(limit),
    staleTime: 60 * 100, // 1 minute
  });
};

export const useEventsByCamera = (cameraId: number, params?: {
  page?: number;
  limit?: number;
  startDate?: string;
  endDate?: string;
  objectType?: string;
  severity?: string;
}) => {
  return useQuery({
    queryKey: EVENT_QUERY_KEYS.byCamera(cameraId, params),
    queryFn: () => eventService.getEventsByCamera(cameraId, params),
    enabled: !!cameraId,
    staleTime: 30 * 100, // 30 seconds
  });
};

export const useEventsStats = (params?: {
  startDate?: string;
  endDate?: string;
  cameraId?: number;
}) => {
  return useQuery({
    queryKey: EVENT_QUERY_KEYS.stats(params),
    queryFn: () => eventService.getEventsStats(params),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

export const useUpdateEventStatus = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, resolved }: { id: number; resolved: boolean }) => 
      eventService.updateEventStatus(id, resolved),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: EVENT_QUERY_KEYS.detail(id) });
      queryClient.invalidateQueries({ queryKey: EVENT_QUERY_KEYS.lists() });
    },
  });
};

export const useDeleteEvent = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => eventService.deleteEvent(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: EVENT_QUERY_KEYS.lists() });
    },
  });
};