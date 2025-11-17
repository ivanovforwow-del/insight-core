import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { alertService } from '../../services/alertService';
import { Alert } from '../../types';

// Ключи запросов для данных оповещений
const ALERT_QUERY_KEYS = {
  all: ['alerts'] as const,
  lists: () => [...ALERT_QUERY_KEYS.all, 'list'] as const,
  list: (params?: any) => [...ALERT_QUERY_KEYS.lists(), params] as const,
  details: () => [...ALERT_QUERY_KEYS.all, 'detail'] as const,
  detail: (id: number) => [...ALERT_QUERY_KEYS.details(), id] as const,
  unreadCount: () => [...ALERT_QUERY_KEYS.all, 'unreadCount'] as const,
  recent: (limit?: number) => [...ALERT_QUERY_KEYS.all, 'recent', limit] as const,
};

export const useAlerts = (params?: {
  page?: number;
  limit?: number;
  startDate?: string;
  endDate?: string;
  type?: string;
  read?: boolean;
  search?: string;
}) => {
  return useQuery({
    queryKey: ALERT_QUERY_KEYS.list(params),
    queryFn: () => alertService.getAlerts(params),
    staleTime: 30 * 100, // 30 секунд
  });
};

export const useAlert = (id: number) => {
  return useQuery({
    queryKey: ALERT_QUERY_KEYS.detail(id),
    queryFn: () => alertService.getAlertById(id),
    enabled: !!id,
  });
};

export const useUnreadAlertsCount = () => {
  return useQuery({
    queryKey: ALERT_QUERY_KEYS.unreadCount(),
    queryFn: () => alertService.getUnreadAlertsCount(),
    staleTime: 10 * 1000, // 10 секунд
  });
};

export const useRecentAlerts = (limit: number = 10) => {
  return useQuery({
    queryKey: ALERT_QUERY_KEYS.recent(limit),
    queryFn: () => alertService.getRecentAlerts(limit),
    staleTime: 60 * 1000, // 1 минута
  });
};

export const useMarkAlertAsRead = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => alertService.markAlertAsRead(id),
    onSuccess: (_, id) => {
      queryClient.invalidateQueries({ queryKey: ALERT_QUERY_KEYS.detail(id) });
      queryClient.invalidateQueries({ queryKey: ALERT_QUERY_KEYS.lists() });
      queryClient.invalidateQueries({ queryKey: ALERT_QUERY_KEYS.unreadCount() });
    },
  });
};

export const useMarkAllAlertsAsRead = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: () => alertService.markAllAlertsAsRead(),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ALERT_QUERY_KEYS.lists() });
      queryClient.invalidateQueries({ queryKey: ALERT_QUERY_KEYS.unreadCount() });
    },
  });
};

export const useDeleteAlert = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => alertService.deleteAlert(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ALERT_QUERY_KEYS.lists() });
      queryClient.invalidateQueries({ queryKey: ALERT_QUERY_KEYS.unreadCount() });
    },
  });
};

export const useDeleteAllAlerts = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: () => alertService.deleteAllAlerts(),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ALERT_QUERY_KEYS.lists() });
      queryClient.invalidateQueries({ queryKey: ALERT_QUERY_KEYS.unreadCount() });
    },
  });
};