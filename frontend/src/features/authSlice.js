import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  access_token: 0,
};

export const authSlice = createSlice({
  name: "auth_token",
  initialState,
  reducers: {
    setUserToken: (state, action) => {
      state.access_token = action.payload.access_token;
    },
    UnsetUserToken: (state, action) => {
      state.access_token = action.payload.access_token;
    },
  },
});

// Action creators are generated for each case reducer function
export const { setUserToken, UnsetUserToken } = authSlice.actions;

export default authSlice.reducer;
