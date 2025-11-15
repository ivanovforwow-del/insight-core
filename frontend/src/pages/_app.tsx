import React from 'react';
import type { AppProps } from 'next/app';
import { ConfigProvider } from 'antd';
import { Provider } from 'react-redux';
import { store } from '../store';
import QueryProvider from '../app/providers/QueryProvider';
import { ThemeProvider } from '../providers/ThemeProvider';

// Import Ant Design styles
import 'antd/dist/reset.css';
import '../styles/globals.css';

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <QueryProvider>
      <Provider store={store}>
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
            <Component {...pageProps} />
          </ConfigProvider>
        </ThemeProvider>
      </Provider>
    </QueryProvider>
  );
}

export default MyApp;