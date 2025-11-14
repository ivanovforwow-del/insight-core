import { ReactNode } from 'react';
import { ConfigProvider } from 'antd';
import { AppProvider } from '@/providers/AppProvider';
import SSRProvider from './ssr-provider';
import type { Metadata } from 'next';

// Import Ant Design styles
import 'antd/dist/reset.css';

export const metadata: Metadata = {
  title: 'InsightCore - Video Analytics Platform',
  description: 'Advanced video analytics and surveillance platform',
};

export default function RootLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <SSRProvider>
          <AppProvider>
            <ConfigProvider
              theme={{
                token: {
                  colorPrimary: '#1890ff',
                  borderRadius: 6,
                },
              }}
            >
              {children}
            </ConfigProvider>
          </AppProvider>
        </SSRProvider>
      </body>
    </html>
  );
}