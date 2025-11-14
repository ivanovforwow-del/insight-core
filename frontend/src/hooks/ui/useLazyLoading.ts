import { useState, useEffect, useRef, useCallback } from 'react';

interface LazyLoadingOptions {
  root?: Element | null;
  rootMargin?: string;
  threshold?: number;
}

export const useLazyLoading = <T extends HTMLElement>(
  callback: () => void,
  options: LazyLoadingOptions = {}
) => {
  const [isIntersecting, setIsIntersecting] = useState(false);
  const elementRef = useRef<T>(null);
  const observerRef = useRef<IntersectionObserver | null>(null);

  const defaultOptions: LazyLoadingOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.1,
    ...options,
  };

  const handleIntersection = useCallback((entries: IntersectionObserverEntry[]) => {
    const [entry] = entries;
    if (entry.isIntersecting) {
      setIsIntersecting(true);
      callback();
      if (observerRef.current && elementRef.current) {
        observerRef.current.unobserve(elementRef.current);
        observerRef.current.disconnect();
        observerRef.current = null;
      }
    }
  }, [callback]);

  useEffect(() => {
    if (elementRef.current) {
      observerRef.current = new IntersectionObserver(
        handleIntersection,
        defaultOptions
      );
      observerRef.current.observe(elementRef.current);
    }

    return () => {
      if (observerRef.current && elementRef.current) {
        observerRef.current.unobserve(elementRef.current);
        observerRef.current.disconnect();
        observerRef.current = null;
      }
    };
  }, [handleIntersection, defaultOptions]);

  return {
    elementRef,
    isIntersecting,
  };
};

// Hook for lazy loading images
export const useLazyImage = (src: string) => {
 const [imageSrc, setImageSrc] = useState('');
  const [isLoading, setIsLoading] = useState(true);
 const [error, setError] = useState(false);

  useEffect(() => {
    const img = new Image();
    img.onload = () => {
      setImageSrc(src);
      setIsLoading(false);
    };
    img.onerror = () => {
      setError(true);
      setIsLoading(false);
    };
    img.src = src;
 }, [src]);

  return { imageSrc, isLoading, error };
};

// Hook for lazy loading components
export const useLazyComponent = <T,>(
  importFn: () => Promise<{ default: React.ComponentType<T> }>,
  fallback?: React.ReactNode
) => {
  const [Component, setComponent] = useState<React.ComponentType<T> | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const loadComponent = async () => {
      try {
        const module = await importFn();
        setComponent(() => module.default);
        setLoading(false);
      } catch (err) {
        setError(err as Error);
        setLoading(false);
      }
    };

    loadComponent();
  }, [importFn]);

  return {
    Component,
    loading,
    error,
    fallback: loading && fallback ? fallback : null,
  };
};