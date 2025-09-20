import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

interface Post {
  id: string;
  author: {
    id: string;
    username: string;
    profileImage: string;
  };
  content: {
    text?: string;
    image?: string;
    video?: string;
  };
  type: string;
  isAIGenerated: boolean;
  aiMetadata?: {
    generatingAgent: string;
    qualityScore: number;
    styleEmulated?: string;
  };
  engagement: {
    likes: any[];
    laughReacts: any[];
    shares: any[];
    saves: any[];
  };
  hashtags: string[];
  createdAt: string;
  comedyMetadata: {
    humorStyle: string;
    topics: string[];
  };
}

interface PostsState {
  posts: Post[];
  recommendations: Post[];
  isLoading: boolean;
  error: string | null;
  hasMore: boolean;
  currentPage: number;
}

const initialState: PostsState = {
  posts: [],
  recommendations: [],
  isLoading: false,
  error: null,
  hasMore: true,
  currentPage: 0,
};

export const fetchFeed = createAsyncThunk(
  'posts/fetchFeed',
  async ({ type, limit = 20, offset = 0 }: { type: string; limit?: number; offset?: number }) => {
    const token = localStorage.getItem('token');
    const response = await axios.get(`${API_URL}/posts`, {
      params: { type, limit, offset },
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
  }
);

export const fetchRecommendations = createAsyncThunk(
  'posts/fetchRecommendations',
  async ({ userId, limit = 20, offset = 0 }: { userId: string; limit?: number; offset?: number }) => {
    const token = localStorage.getItem('token');
    const response = await axios.get(`${API_URL}/recommendations`, {
      params: { limit },
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
  }
);

export const likePost = createAsyncThunk(
  'posts/likePost',
  async (data: any) => {
    const token = localStorage.getItem('token');
    const postId = typeof data === 'string' ? data : data.postId;
    const response = await axios.post(
      `${API_URL}/posts/${postId}/like`,
      {},
      { headers: { Authorization: `Bearer ${token}` } }
    );
    return response.data;
  }
);

export const sharePost = createAsyncThunk(
  'posts/sharePost',
  async (postId: string) => {
    return { postId, shared: true };
  }
);

export const savePost = createAsyncThunk(
  'posts/savePost',
  async (postId: string) => {
    return { postId, saved: true };
  }
);

const postsSlice = createSlice({
  name: 'posts',
  initialState,
  reducers: {
    clearPosts: (state) => {
      state.posts = [];
      state.currentPage = 0;
      state.hasMore = true;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchFeed.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(fetchFeed.fulfilled, (state, action) => {
        state.isLoading = false;
        if (state.currentPage === 0) {
          state.posts = action.payload;
        } else {
          state.posts = [...state.posts, ...action.payload];
        }
        state.hasMore = action.payload.length === 20;
        state.currentPage += 1;
      })
      .addCase(fetchFeed.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || 'Failed to fetch posts';
      })
      .addCase(fetchRecommendations.fulfilled, (state, action) => {
        state.isLoading = false;
        state.recommendations = action.payload;
        state.posts = action.payload;
      })
      .addCase(likePost.fulfilled, (state, action) => {
        const index = state.posts.findIndex(p => p.id === action.payload.id);
        if (index !== -1) {
          state.posts[index] = action.payload;
        }
      });
  },
});

export const { clearPosts } = postsSlice.actions;
export default postsSlice.reducer;