// This file is no longer used as we're migrating to Next.js App Router
// Keeping it for reference during the transition period

import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ConfigProvider } from 'antd';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

// Layout components
import Layout from './components/Layout/Layout';
import Dashboard from './pages/Dashboard/Dashboard';
// Removed Cameras import since we're migrating to Next.js App Router
import Events from './pages/Events/Events';
import Analytics from './pages/Analytics/Analytics';
import Alerts from './pages/Alerts/Alerts';
import VideoPlayer from './pages/VideoPlayer/VideoPlayer';
// Removed Settings import since the file doesn't exist

// Removed authentication components since the files don't exist
// import Login from './pages/Auth/Login';
// import Register from './pages/Auth/Register';

// API client configuration
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
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
            {/* Removed public routes since the files don't exist */}
            {/* <Route path="/login" element={<Login />} /> */}
            {/* <Route path="/register" element={<Register />} /> */}
            
            {/* Protected routes */}
            <Route path="/" element={<Layout />}>
              <Route index element={<Dashboard />} />
              <Route path="dashboard" element={<Dashboard />} />
              {/* Removed cameras route as it's now handled by Next.js App Router */}
              <Route path="events" element={<Events />} />
              <Route path="analytics" element={<Analytics />} />
              <Route path="alerts" element={<Alerts />} />
              <Route path="video-player" element={<VideoPlayer />} />
              {/* Removed settings route since the file doesn't exist */}
            </Route>
          </Routes>
        </Router>
      </ConfigProvider>
    </QueryClientProvider>
  );
}

export default App;