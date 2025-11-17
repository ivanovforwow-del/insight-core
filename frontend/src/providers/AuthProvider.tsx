'use client';

import React, { ReactNode, useEffect, useState } from 'react';
import { authService } from '../services/authService';
import { useRouter, usePathname } from 'next/navigation';

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [loading, setLoading] = useState(true);
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    // Для страницы входа не выполнять проверку аутентификации
    if (pathname === '/login') {
      setLoading(false);
      return;
    }

    // Для других страниц проверять аутентификацию
    if (!authService.isAuthenticated()) {
      // Redirect to login page
      router.push('/login');
      return;
    }

    setLoading(false);
  }, [pathname, router]);

  // Показать состояние загрузки во время проверки аутентификации
  if (loading) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '100vh' 
      }}>
        <div>Загрузка...</div>
      </div>
    );
  }

  return <>{children}</>;
};