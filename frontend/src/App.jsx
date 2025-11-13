import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ConfigProvider } from 'antd';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';

// Layout components
import Layout from './components/Layout/Layout';
import Dashboard from './pages/Dashboard/Dashboard';
import Cameras from './pages/Cameras/Cameras';
import Events from './pages/Events/Events';
import Analytics from './pages/Analytics/Analytics';
import Alerts from './pages/Alerts/Alerts';
import VideoPlayer from './pages/VideoPlayer/VideoPlayer';
import Settings from './pages/Settings/Settings';

// Authentication components
import Login from './pages/Auth/Login';
import Register from './pages/Auth/Register';

// API client configuration
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 100, // 10 minutes
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ConfigProvider
        theme={{
          token: {
            colorPrimary: '#1890ff',
            borderRadius: 6,
          },
        }}
      >
        <Router>
          <Routes>
            {/* Public routes */}
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            
            {/* Protected routes */}
            <Route path="/" element={<Layout />}>
              <Route index element={<Dashboard />} />
              <Route path="dashboard" element={<Dashboard />} />
              <Route path="cameras" element={<Cameras />} />
              <Route path="events" element={<Events />} />
              <Route path="analytics" element={<Analytics />} />
              <Route path="alerts" element={<Alerts />} />
              <Route path="video-player" element={<VideoPlayer />} />
              <Route path="settings" element={<Settings />} />
            </Route>
          </Routes>
        </Router>
      </ConfigProvider>
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}

export default App;