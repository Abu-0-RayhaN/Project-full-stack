import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const userAuthApi = createApi({
  reducerPath: "userAuthApi",
  baseQuery: fetchBaseQuery({ baseUrl: "http://127.0.0.1:8000/api/user/" }),
  endpoints: (builder) => ({
    registerUser: builder.mutation({
      query: (user) => ({
        url: "register/",
        method: "POST",
        body: user,
        headers: {
          "Content-type": "application/json",
        },
      }),
    }),
    loginUser: builder.mutation({
      query: (user) => ({
        url: "login/",
        method: "POST",
        body: user,
        headers: {
          "Content-type": "application/json",
        },
      }),
    }),
  }),
});

export const { useRegisterUserMutation, useLoginUserMutation } = userAuthApi;