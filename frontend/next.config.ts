import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  /* параметры конфигурации здесь */
  output: 'export', // Enable static export
  trailingSlash: true, // Add trailing slashes to URLs
  images: {
    unoptimized: true, // Disable image optimization for static export
  },
  env: {
    REACT_APP_API_URL: process.env.REACT_APP_API_URL || '/api',
  },
  webpack: (config, { isServer }) => {
    // Важно: Возвращаем измененную конфигурацию
    if (!isServer) {
      // Устанавливаем внешние зависимости webpack для работы video.js в Next.js
      config.resolve.fallback = {
        ...config.resolve.fallback,
        fs: false,
        net: false,
        tls: false,
      };
    }
    return config;
  },
  // Явно включаем режим webpack и отключаем turbopack
  experimental: {
    webpackBuildWorker: true,
  },
  // Явно отключаем turbopack для принудительного использования webpack
  // Мы используем пустой объект, чтобы удовлетворить требования типа при отключении turbopack
  turbopack: {} as any,
};

export default nextConfig;