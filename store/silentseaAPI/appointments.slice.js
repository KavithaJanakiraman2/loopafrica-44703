import { createSlice, createAsyncThunk } from "@reduxjs/toolkit"
import { apiService } from "./api"
export const api_v1_appointments_list = createAsyncThunk(
  "appointments/api_v1_appointments_list",
  async payload => {
    const response = await apiService.api_v1_appointments_list(payload)
    return response.data
  }
)
export const api_v1_appointments_retrieve = createAsyncThunk(
  "appointments/api_v1_appointments_retrieve",
  async payload => {
    const response = await apiService.api_v1_appointments_retrieve(payload)
    return response.data
  }
)
export const api_v1_appointments_create_create = createAsyncThunk(
  "appointments/api_v1_appointments_create_create",
  async payload => {
    const response = await apiService.api_v1_appointments_create_create(payload)
    return response.data
  }
)
export const api_v1_appointments_todo_appointments_retrieve = createAsyncThunk(
  "appointments/api_v1_appointments_todo_appointments_retrieve",
  async payload => {
    const response = await apiService.api_v1_appointments_todo_appointments_retrieve(
      payload
    )
    return response.data
  }
)
export const api_v1_appointments_update_feedback_partial_update = createAsyncThunk(
  "appointments/api_v1_appointments_update_feedback_partial_update",
  async payload => {
    const response = await apiService.api_v1_appointments_update_feedback_partial_update(
      payload
    )
    return response.data
  }
)
const initialState = { entities: [], api: { loading: "idle", error: null } }
const appointmentsSlice = createSlice({
  name: "appointments",
  initialState,
  reducers: {},
  extraReducers: builder => {
    builder
      .addCase(api_v1_appointments_list.pending, (state, action) => {
        if (state.api.loading === "idle") {
          state.api.loading = "pending"
        }
      })
      .addCase(api_v1_appointments_list.fulfilled, (state, action) => {
        if (state.api.loading === "pending") {
          state.entities = action.payload
          state.api.loading = "idle"
        }
      })
      .addCase(api_v1_appointments_list.rejected, (state, action) => {
        if (state.api.loading === "pending") {
          state.api.error = action.error
          state.api.loading = "idle"
        }
      })
      .addCase(api_v1_appointments_retrieve.pending, (state, action) => {
        if (state.api.loading === "idle") {
          state.api.loading = "pending"
        }
      })
      .addCase(api_v1_appointments_retrieve.fulfilled, (state, action) => {
        if (state.api.loading === "pending") {
          state.entities = [
            ...state.entities.filter(record => record.id !== action.payload.id),
            action.payload
          ]
          state.api.loading = "idle"
        }
      })
      .addCase(api_v1_appointments_retrieve.rejected, (state, action) => {
        if (state.api.loading === "pending") {
          state.api.error = action.error
          state.api.loading = "idle"
        }
      })
      .addCase(api_v1_appointments_create_create.pending, (state, action) => {
        if (state.api.loading === "idle") {
          state.api.loading = "pending"
        }
      })
      .addCase(api_v1_appointments_create_create.fulfilled, (state, action) => {
        if (state.api.loading === "pending") {
          state.entities.push(action.payload)
          state.api.loading = "idle"
        }
      })
      .addCase(api_v1_appointments_create_create.rejected, (state, action) => {
        if (state.api.loading === "pending") {
          state.api.error = action.error
          state.api.loading = "idle"
        }
      })
      .addCase(
        api_v1_appointments_todo_appointments_retrieve.pending,
        (state, action) => {
          if (state.api.loading === "idle") {
            state.api.loading = "pending"
          }
        }
      )
      .addCase(
        api_v1_appointments_todo_appointments_retrieve.fulfilled,
        (state, action) => {
          if (state.api.loading === "pending") {
            state.entities = [
              ...state.entities.filter(
                record => record.id !== action.payload.id
              ),
              action.payload
            ]
            state.api.loading = "idle"
          }
        }
      )
      .addCase(
        api_v1_appointments_todo_appointments_retrieve.rejected,
        (state, action) => {
          if (state.api.loading === "pending") {
            state.api.error = action.error
            state.api.loading = "idle"
          }
        }
      )
      .addCase(
        api_v1_appointments_update_feedback_partial_update.pending,
        (state, action) => {
          if (state.api.loading === "idle") {
            state.api.loading = "pending"
          }
        }
      )
      .addCase(
        api_v1_appointments_update_feedback_partial_update.fulfilled,
        (state, action) => {
          if (state.api.loading === "pending") {
            state.entities = state.entities.map(record =>
              record.id === action.payload.id ? action.payload : record
            )
            state.api.loading = "idle"
          }
        }
      )
      .addCase(
        api_v1_appointments_update_feedback_partial_update.rejected,
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
  api_v1_appointments_list,
  api_v1_appointments_retrieve,
  api_v1_appointments_create_create,
  api_v1_appointments_todo_appointments_retrieve,
  api_v1_appointments_update_feedback_partial_update,
  slice: appointmentsSlice
}
