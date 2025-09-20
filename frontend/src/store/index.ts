import { configureStore } from '@reduxjs/toolkit';
import authSlice from './authSlice';
import postsSlice from './postsSlice';
import preferencesSlice from './preferencesSlice';

export const store = configureStore({
  reducer: {
    auth: authSlice,
    posts: postsSlice,
    preferences: preferencesSlice,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;