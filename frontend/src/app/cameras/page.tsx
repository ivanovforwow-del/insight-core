import React from 'react';
import { Metadata } from 'next';
import SSRCameras from '../components/SSRCameras';
import { Camera } from '@/types';

// Функция получения тестовых данных для SSR
async function fetchCameras(): Promise<Camera[]> {
  // Имитация задержки вызова API
  await new Promise(resolve => setTimeout(resolve, 100));
  
  return [
    {
      id: 1,
      name: 'Камера 1 (вход)',
      rtspUrl: 'rtsp://192.168.1.100:554/stream1',
      location: 'Главный вход',
      status: 'active',
      vendor: 'Hikvision',
      streamSettings: {
        fps: 30,
        resolution: '1920x1080',
      },
      zones: 3,
      lines: 2,
      rules: 5,
      enabled: true,
    },
    {
      id: 2,
      name: 'Камера 2 (парковка)',
      rtspUrl: 'rtsp://192.168.1.101:554/stream1',
      location: 'Парковочная зона',
      status: 'active',
      vendor: 'Dahua',
      streamSettings: {
        fps: 25,
        resolution: '1280x720',
      },
      zones: 2,
      lines: 1,
      rules: 3,
      enabled: true,
    },
    {
      id: 3,
      name: 'Камера 3 (ворота)',
      rtspUrl: 'rtsp://192.168.1.102:554/stream1',
      location: 'Главные ворота',
      status: 'inactive',
      vendor: 'Axis',
      streamSettings: {
        fps: 20,
        resolution: '1920x1080',
      },
      zones: 1,
      lines: 0,
      rules: 2,
      enabled: false,
    },
    {
      id: 4,
      name: 'Камера 1 (склад)',
      rtspUrl: 'rtsp://192.168.1.103:554/stream1',
      location: 'Склад',
      status: 'error',
      vendor: 'Bosch',
      streamSettings: {
        fps: 15,
        resolution: '1280x720',
      },
      zones: 4,
      lines: 3,
      rules: 6,
      enabled: true,
    },
  ];
}

export const metadata: Metadata = {
  title: 'Камеры | InsightCore',
  description: 'Управление и мониторинг камер безопасности',
};

const CamerasPage = async () => {
  const cameras = await fetchCameras();

  return <SSRCameras cameras={cameras} />;
};

export default CamerasPage;