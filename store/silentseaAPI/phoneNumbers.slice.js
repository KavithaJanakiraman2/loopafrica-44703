import { createSlice, createAsyncThunk } from "@reduxjs/toolkit"
import { apiService } from "./api"
export const modules_twofactorauth_send_otp_create = createAsyncThunk(
  "phoneNumbers/modules_twofactorauth_send_otp_create",
  async payload => {
    const response = await apiService.modules_twofactorauth_send_otp_create(
      payload
    )
    return response.data
  }
)
const initialState = { entities: [], api: { loading: "idle", error: null } }
const phoneNumbersSlice = createSlice({
  name: "phoneNumbers",
  initialState,
  reducers: {},
  extraReducers: builder => {
    builder
      .addCase(
        modules_twofactorauth_send_otp_create.pending,
        (state, action) => {
          if (state.api.loading === "idle") {
            state.api.loading = "pending"
          }
        }
      )
      .addCase(
        modules_twofactorauth_send_otp_create.fulfilled,
        (state, action) => {
          if (state.api.loading === "pending") {
            state.entities.push(action.payload)
            state.api.loading = "idle"
          }
        }
      )
      .addCase(
        modules_twofactorauth_send_otp_create.rejected,
        (state, action) => {
          if (state.api.loading === "pending") {
            state.api.error = action.error
            state.api.loading = "idle"
          }
        }
      )
  }
})
export default {
  modules_twofactorauth_send_otp_create,
  slice: phoneNumbersSlice
}
