import { createSlice, createAsyncThunk } from "@reduxjs/toolkit"
import { apiService } from "./api"
export const api_v1_doctors_list = createAsyncThunk(
  "paginatedDoctorLists/api_v1_doctors_list",
  async payload => {
    const response = await apiService.api_v1_doctors_list(payload)
    return response.data
  }
)
const initialState = { entities: [], api: { loading: "idle", error: null } }
const paginatedDoctorListsSlice = createSlice({
  name: "paginatedDoctorLists",
  initialState,
  reducers: {},
  extraReducers: builder => {
    builder
      .addCase(api_v1_doctors_list.pending, (state, action) => {
        if (state.api.loading === "idle") {
          state.api.loading = "pending"
        }
      })
      .addCase(api_v1_doctors_list.fulfilled, (state, action) => {
        if (state.api.loading === "pending") {
          state.entities = [
            ...state.entities.filter(record => record.id !== action.payload.id),
            action.payload
          ]
          state.api.loading = "idle"
        }
      })
      .addCase(api_v1_doctors_list.rejected, (state, action) => {
        if (state.api.loading === "pending") {
          state.api.error = action.error
          state.api.loading = "idle"
        }
      })
  }
})
export default { api_v1_doctors_list, slice: paginatedDoctorListsSlice }
