'use client';

import React, { ReactNode } from 'react';
import { ConfigProvider } from 'antd';
import { ThemeProvider } from './ThemeProvider';
import { QueryProvider } from './QueryProvider';
import { Provider } from 'react-redux';
import { store } from '@/store';

// Import Ant Design styles
import 'antd/dist/reset.css';
import '@/styles/globals.css';

interface AppProviderProps {
  children: ReactNode;
}

export const AppProvider: React.FC<AppProviderProps> = ({ children }) => {
  return (
    <Provider store={store}>
      <QueryProvider>
        <ThemeProvider>
          <ConfigProvider
            theme={{
              token: {
                colorPrimary: '#1890ff',
                borderRadius: 6,
                fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
              },
              components: {
                Layout: {
                  colorBgHeader: '#ffffff',
                  colorBgBody: '#f0f2f5',
                  colorBgTrigger: '#1890ff',
                },
                Card: {
                  colorBgContainer: '#ffffff',
                  borderRadiusLG: 8,
                  borderRadiusSM: 6,
                },
                Table: {
                  cellPaddingInline: 16,
                  cellPaddingBlock: 12,
                  colorBgContainer: '#ffffff',
                  borderRadiusLG: 8,
                },
                Button: {
                  controlHeight: 32,
                  controlHeightLG: 40,
                  controlHeightSM: 24,
                  borderRadius: 6,
                },
              },
            }}
          >
            {children}
          </ConfigProvider>
        </ThemeProvider>
      </QueryProvider>
    </Provider>
  );
};