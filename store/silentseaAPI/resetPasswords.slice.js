import { createSlice, createAsyncThunk } from "@reduxjs/toolkit"
import { apiService } from "./api"
export const api_v1_resetpassword_create = createAsyncThunk(
  "resetPasswords/api_v1_resetpassword_create",
  async payload => {
    const response = await apiService.api_v1_resetpassword_create(payload)
    return response.data
  }
)
const initialState = { entities: [], api: { loading: "idle", error: null } }
const resetPasswordsSlice = createSlice({
  name: "resetPasswords",
  initialState,
  reducers: {},
  extraReducers: builder => {
    builder
      .addCase(api_v1_resetpassword_create.pending, (state, action) => {
        if (state.api.loading === "idle") {
          state.api.loading = "pending"
        }
      })
      .addCase(api_v1_resetpassword_create.fulfilled, (state, action) => {
        if (state.api.loading === "pending") {
          state.entities.push(action.payload)
          state.api.loading = "idle"
        }
      })
      .addCase(api_v1_resetpassword_create.rejected, (state, action) => {
        if (state.api.loading === "pending") {
          state.api.error = action.error
          state.api.loading = "idle"
        }
      })
  }
})
export default { api_v1_resetpassword_create, slice: resetPasswordsSlice }
