// Глобальные типы для фронтенда InsightCore

// Импорт React для определения типов
import React from 'react';

// User types
export interface User {
  id?: number;
  name: string;
  email: string;
  role?: string;
  avatar?: string;
}

// Camera types
export interface Camera {
  id: number;
  name: string;
 rtspUrl: string;
  location: string;
  status: 'active' | 'inactive' | 'error' | 'maintenance';
  vendor: string;
  streamSettings: {
    fps: number;
    resolution: string;
 };
  zones: number;
  lines: number;
  rules: number;
  enabled?: boolean;
}

// Event types
export interface Event {
  id: number;
  cameraId: number;
  cameraName: string;
  objectType: string;
  timestamp: string;
  confidence: number;
  severity: 'low' | 'medium' | 'high' | 'critical';
 imageUrl?: string;
  metadata?: Record<string, any>;
}

// Alert types
export interface Alert {
  id: number;
  title: string;
  message: string;
  type: 'info' | 'warning' | 'error' | 'success';
  timestamp: string;
  read: boolean;
  eventId?: number;
}

// Analytics types
export interface AnalyticsData {
  totalCameras: number;
  activeCameras: number;
 totalEvents: number;
  eventsToday: number;
  alertsToday: number;
  totalVideos: number;
  processingTime: string;
  systemUptime: string;
}

export interface EventByType {
  name: string;
  value: number;
}

export interface EventByHour {
  hour: string;
 events: number;
}

// Video types
export interface Video {
  id: number;
  name: string;
 cameraId: number;
  cameraName: string;
  startTime: string;
 endTime: string;
 duration: number;
 size: number;
  format: string;
  url: string;
  thumbnailUrl?: string;
}

// Form types
export interface CameraFormData {
  name: string;
  rtspUrl: string;
  location: string;
  status: string;
  vendor: string;
  enabled?: boolean;
}

// API Response types
export interface ApiResponse<T> {
  data: T;
  message?: string;
  success: boolean;
}

// Component prop types
export interface ProtectedRouteProps {
  children: React.ReactNode;
}

export interface NotificationProps {
  notifications: Alert[];
  onMarkAsRead?: (id: number) => void;
 onClearAll?: () => void;
}