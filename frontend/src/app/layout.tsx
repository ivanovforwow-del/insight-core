import { ReactNode } from 'react';
import { ConfigProvider } from 'antd';
import { AppProvider } from '@/providers/AppProvider';
import SSRProvider from './ssr-provider';
import type { Metadata } from 'next';

// Импорт стилей Ant Design
import 'antd/dist/reset.css';

export const metadata: Metadata = {
 title: 'InsightCore - Платформа видеоаналитики',
  description: 'Передовая платформа видеоаналитики и наблюдения',
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
            {children}
          </AppProvider>
        </SSRProvider>
      </body>
    </html>
  );
}