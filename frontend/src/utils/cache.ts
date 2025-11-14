// Cache utilities for the InsightCore frontend
import React from 'react';

// In-memory cache implementation
class InMemoryCache<T = any> {
  private cache: Map<string, { data: T; timestamp: number; ttl: number }> = new Map();

  set(key: string, data: T, ttl: number = 300000): void { // Default TTL: 5 minutes
    this.cache.set(key, {
      data,
      timestamp: Date.now(),
      ttl,
    });
  }

  get(key: string): T | null {
    const item = this.cache.get(key);
    if (!item) {
      return null;
    }

    // Check if item has expired
    if (Date.now() - item.timestamp > item.ttl) {
      this.cache.delete(key);
      return null;
    }

    return item.data;
  }

 has(key: string): boolean {
    const item = this.cache.get(key);
    if (!item) {
      return false;
    }

    // Check if item has expired
    if (Date.now() - item.timestamp > item.ttl) {
      this.cache.delete(key);
      return false;
    }

    return true;
  }

  delete(key: string): boolean {
    return this.cache.delete(key);
  }

  clear(): void {
    this.cache.clear();
  }

  size(): number {
    return this.cache.size;
  }

  // Garbage collection for expired items
  gc(): void {
    const now = Date.now();
    for (const [key, item] of this.cache.entries()) {
      if (now - item.timestamp > item.ttl) {
        this.cache.delete(key);
      }
    }
  }
}

// LocalStorage cache implementation
class LocalStorageCache<T = any> {
  private prefix: string;

  constructor(prefix: string = 'insightcore') {
    this.prefix = prefix;
  }

  private getKey(key: string): string {
    return `${this.prefix}:${key}`;
  }

  set(key: string, data: T, ttl: number = 30000): void { // Default TTL: 5 minutes
    const item = {
      data,
      timestamp: Date.now(),
      ttl,
    };
    try {
      localStorage.setItem(this.getKey(key), JSON.stringify(item));
    } catch (error) {
      console.warn('Failed to set item in localStorage:', error);
    }
 }

  get(key: string): T | null {
    try {
      const itemStr = localStorage.getItem(this.getKey(key));
      if (!itemStr) {
        return null;
      }

      const item = JSON.parse(itemStr);
      
      // Check if item has expired
      if (Date.now() - item.timestamp > item.ttl) {
        localStorage.removeItem(this.getKey(key));
        return null;
      }

      return item.data;
    } catch (error) {
      console.warn('Failed to get item from localStorage:', error);
      return null;
    }
  }

  has(key: string): boolean {
    const item = this.get(key);
    return item !== null;
  }

  delete(key: string): boolean {
    try {
      localStorage.removeItem(this.getKey(key));
      return true;
    } catch (error) {
      console.warn('Failed to delete item from localStorage:', error);
      return false;
    }
  }

  clear(): void {
    try {
      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (key && key.startsWith(this.prefix)) {
          localStorage.removeItem(key);
        }
      }
    } catch (error) {
      console.warn('Failed to clear localStorage:', error);
    }
 }
}

// Cache manager combining both in-memory and localStorage
class CacheManager {
  private inMemoryCache: InMemoryCache;
  private localStorageCache: LocalStorageCache;

  constructor() {
    this.inMemoryCache = new InMemoryCache();
    this.localStorageCache = new LocalStorageCache();
  }

  // Set value in both caches
  set(key: string, data: any, ttl: number = 300000): void {
    this.inMemoryCache.set(key, data, ttl);
    this.localStorageCache.set(key, data, ttl);
  }

  // Get value, prioritize in-memory cache
  get<T = any>(key: string): T | null {
    // First check in-memory cache
    let data = this.inMemoryCache.get(key) as T | null;
    if (data !== null) {
      return data;
    }

    // If not found in memory, check localStorage and populate memory
    data = this.localStorageCache.get(key) as T | null;
    if (data !== null) {
      // Repopulate in-memory cache with data from localStorage
      const localStorageItem = localStorage.getItem(`insightcore:${key}`);
      if (localStorageItem) {
        const item = JSON.parse(localStorageItem);
        this.inMemoryCache.set(key, data, item.ttl);
      }
    }

    return data;
  }

  has(key: string): boolean {
    return this.inMemoryCache.has(key) || this.localStorageCache.has(key);
  }

  delete(key: string): boolean {
    const inMemoryResult = this.inMemoryCache.delete(key);
    const localStorageResult = this.localStorageCache.delete(key);
    return inMemoryResult || localStorageResult;
 }

  clear(): void {
    this.inMemoryCache.clear();
    this.localStorageCache.clear();
  }

  // Garbage collection for expired items in both caches
  gc(): void {
    this.inMemoryCache.gc();
  }
}

// Create singleton instance
export const cacheManager = new CacheManager();

// Cache hook for React components
export const useCache = <T>(key: string, initialValue?: T) => {
  const [cachedValue, setCachedValue] = React.useState<T>(() => {
    const cached = cacheManager.get<T>(key);
    return cached !== null ? cached : initialValue as T;
  });

  const setValue = React.useCallback((value: T) => {
    cacheManager.set(key, value);
    setCachedValue(value);
  }, [key]);

  return [cachedValue, setValue] as const;
};

// Export types
export type { InMemoryCache, LocalStorageCache, CacheManager };