'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function HomePage() {
  const router = useRouter();

 useEffect(() => {
    // Перенаправляем на страницу логина
    router.push('/login');
  }, [router]);

  return null; // или можно показать простой индикатор загрузки
}