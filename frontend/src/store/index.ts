import { configureStore } from '@reduxjs/toolkit';
import { setupListeners } from '@reduxjs/toolkit/query';
import apiClient from '../services/api';
import { queryClient } from '../services/api';

// Create Redux store
export const store = configureStore({
  reducer: {
    // Add reducers here
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      thunk: {
        extraArgument: { apiClient, queryClient },
      },
    }),
});

// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

// Enable listener behavior for refetchOnFocus/refetchOnReconnect
setupListeners(store.dispatch);