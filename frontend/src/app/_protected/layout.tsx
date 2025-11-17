'use client';

import React from 'react';
import { AppProvider } from '@/providers/AppProvider';
import { AuthProvider } from '@/providers/AuthProvider';
import type { ReactNode } from 'react';

interface ProtectedLayoutProps {
  children: ReactNode;
}

export default function ProtectedLayout({
  children,
}: ProtectedLayoutProps) {
  return (
    <AuthProvider>
      <AppProvider>
        {children}
      </AppProvider>
    </AuthProvider>
  );
}