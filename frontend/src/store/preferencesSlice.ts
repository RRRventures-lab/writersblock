import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface PreferencesState {
  humorStyles: string[];
  favoriteTopics: string[];
  preferredFormats: string[];
  comedyPersonality: string;
  autoGenerateContent: boolean;
}

const initialState: PreferencesState = {
  humorStyles: [],
  favoriteTopics: [],
  preferredFormats: [],
  comedyPersonality: 'witty',
  autoGenerateContent: true,
};

const preferencesSlice = createSlice({
  name: 'preferences',
  initialState,
  reducers: {
    setHumorStyles: (state, action: PayloadAction<string[]>) => {
      state.humorStyles = action.payload;
    },
    setFavoriteTopics: (state, action: PayloadAction<string[]>) => {
      state.favoriteTopics = action.payload;
    },
    setPreferredFormats: (state, action: PayloadAction<string[]>) => {
      state.preferredFormats = action.payload;
    },
    setComedyPersonality: (state, action: PayloadAction<string>) => {
      state.comedyPersonality = action.payload;
    },
    setAutoGenerate: (state, action: PayloadAction<boolean>) => {
      state.autoGenerateContent = action.payload;
    },
  },
});

export const {
  setHumorStyles,
  setFavoriteTopics,
  setPreferredFormats,
  setComedyPersonality,
  setAutoGenerate,
} = preferencesSlice.actions;

export default preferencesSlice.reducer;