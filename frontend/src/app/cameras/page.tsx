import React from 'react';
import { Metadata } from 'next';
import SSRCameras from '../components/SSRCameras';
import { Camera } from '@/types';

// Mock data fetching function for SSR
async function fetchCameras(): Promise<Camera[]> {
  // Simulate API call delay
  await new Promise(resolve => setTimeout(resolve, 100));
  
  return [
    {
      id: 1,
      name: 'Entrance Cam 1',
      rtspUrl: 'rtsp://192.168.1.100:554/stream1',
      location: 'Main Entrance',
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
      name: 'Parking Cam 2',
      rtspUrl: 'rtsp://192.168.1.101:554/stream1',
      location: 'Parking Area',
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
      name: 'Gate Cam 3',
      rtspUrl: 'rtsp://192.168.1.102:554/stream1',
      location: 'Main Gate',
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
      name: 'Warehouse Cam 1',
      rtspUrl: 'rtsp://192.168.1.103:554/stream1',
      location: 'Warehouse',
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
  title: 'Cameras | InsightCore',
  description: 'Manage and monitor security cameras',
};

const CamerasPage = async () => {
  const cameras = await fetchCameras();

  return <SSRCameras cameras={cameras} />;
};

export default CamerasPage;