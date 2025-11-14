import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  /* config options here */
  output: 'export', // Enable static export
  trailingSlash: true, // Add trailing slashes to URLs
  images: {
    unoptimized: true, // Disable image optimization for static export
  },
  env: {
    REACT_APP_API_URL: process.env.REACT_APP_API_URL || '/api',
  },
  webpack: (config, { isServer }) => {
    // Important: Return the modified config
    if (!isServer) {
      // Set webpack externals for video.js to work in Next.js
      config.resolve.fallback = {
        ...config.resolve.fallback,
        fs: false,
        net: false,
        tls: false,
      };
    }
    return config;
  },
  // Explicitly enable webpack mode and disable turbopack
  experimental: {
    webpackBuildWorker: true,
  },
  // Explicitly disable turbopack to force webpack
  // We use an empty object to satisfy the type requirement while disabling turbopack
  turbopack: {} as any,
};

export default nextConfig;