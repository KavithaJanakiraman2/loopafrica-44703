import { createSlice, createAsyncThunk } from "@reduxjs/toolkit"
import { apiService } from "./api"
export const api_v1_todo_list = createAsyncThunk(
  "toDOLists/api_v1_todo_list",
  async payload => {
    const response = await apiService.api_v1_todo_list(payload)
    return response.data
  }
)
export const api_v1_todo_create = createAsyncThunk(
  "toDOLists/api_v1_todo_create",
  async payload => {
    const response = await apiService.api_v1_todo_create(payload)
    return response.data
  }
)
export const api_v1_todo_retrieve = createAsyncThunk(
  "toDOLists/api_v1_todo_retrieve",
  async payload => {
    const response = await apiService.api_v1_todo_retrieve(payload)
    return response.data
  }
)
export const api_v1_todo_update = createAsyncThunk(
  "toDOLists/api_v1_todo_update",
  async payload => {
    const response = await apiService.api_v1_todo_update(payload)
    return response.data
  }
)
export const api_v1_todo_partial_update = createAsyncThunk(
  "toDOLists/api_v1_todo_partial_update",
  async payload => {
    const response = await apiService.api_v1_todo_partial_update(payload)
    return response.data
  }
)
export const api_v1_todo_destroy = createAsyncThunk(
  "toDOLists/api_v1_todo_destroy",
  async payload => {
    const response = await apiService.api_v1_todo_destroy(payload)
    return response.data
  }
)
const initialState = { entities: [], api: { loading: "idle", error: null } }
const toDOListsSlice = createSlice({
  name: "toDOLists",
  initialState,
  reducers: {},
  extraReducers: builder => {
    builder
      .addCase(api_v1_todo_list.pending, (state, action) => {
        if (state.api.loading === "idle") {
          state.api.loading = "pending"
        }
      })
      .addCase(api_v1_todo_list.fulfilled, (state, action) => {
        if (state.api.loading === "pending") {
          state.entities = action.payload
          state.api.loading = "idle"
        }
      })
      .addCase(api_v1_todo_list.rejected, (state, action) => {
        if (state.api.loading === "pending") {
          state.api.error = action.error
          state.api.loading = "idle"
        }
      })
      .addCase(api_v1_todo_create.pending, (state, action) => {
        if (state.api.loading === "idle") {
          state.api.loading = "pending"
        }
      })
      .addCase(api_v1_todo_create.fulfilled, (state, action) => {
        if (state.api.loading === "pending") {
          state.entities.push(action.payload)
          state.api.loading = "idle"
        }
      })
      .addCase(api_v1_todo_create.rejected, (state, action) => {
        if (state.api.loading === "pending") {
          state.api.error = action.error
          state.api.loading = "idle"
        }
      })
      .addCase(api_v1_todo_retrieve.pending, (state, action) => {
        if (state.api.loading === "idle") {
          state.api.loading = "pending"
        }
      })
      .addCase(api_v1_todo_retrieve.fulfilled, (state, action) => {
        if (state.api.loading === "pending") {
          state.entities = [
            ...state.entities.filter(record => record.id !== action.payload.id),
            action.payload
          ]
          state.api.loading = "idle"
        }
      })
      .addCase(api_v1_todo_retrieve.rejected, (state, action) => {
        if (state.api.loading === "pending") {
          state.api.error = action.error
          state.api.loading = "idle"
        }
      })
      .addCase(api_v1_todo_update.pending, (state, action) => {
        if (state.api.loading === "idle") {
          state.api.loading = "pending"
        }
      })
      .addCase(api_v1_todo_update.fulfilled, (state, action) => {
        if (state.api.loading === "pending") {
          state.entities = state.entities.map(record =>
            record.id === action.payload.id ? action.payload : record
          )
          state.api.loading = "idle"
        }
      })
      .addCase(api_v1_todo_update.rejected, (state, action) => {
        if (state.api.loading === "pending") {
          state.api.error = action.error
          state.api.loading = "idle"
        }
      })
      .addCase(api_v1_todo_partial_update.pending, (state, action) => {
        if (state.api.loading === "idle") {
          state.api.loading = "pending"
        }
      })
      .addCase(api_v1_todo_partial_update.fulfilled, (state, action) => {
        if (state.api.loading === "pending") {
          state.entities = state.entities.map(record =>
            record.id === action.payload.id ? action.payload : record
          )
          state.api.loading = "idle"
        }
      })
      .addCase(api_v1_todo_partial_update.rejected, (state, action) => {
        if (state.api.loading === "pending") {
          state.api.error = action.error
          state.api.loading = "idle"
        }
      })
      .addCase(api_v1_todo_destroy.pending, (state, action) => {
        if (state.api.loading === "idle") {
          state.api.loading = "pending"
        }
      })
      .addCase(api_v1_todo_destroy.fulfilled, (state, action) => {
        if (state.api.loading === "pending") {
          state.entities = state.entities.filter(
            record => record.id !== action.meta.arg?.id
          )
          state.api.loading = "idle"
        }
      })
      .addCase(api_v1_todo_destroy.rejected, (state, action) => {
        if (state.api.loading === "pending") {
          state.api.error = action.error
          state.api.loading = "idle"
        }
      })
  }
})
export default {
  api_v1_todo_list,
  api_v1_todo_create,
  api_v1_todo_retrieve,
  api_v1_todo_update,
  api_v1_todo_partial_update,
  api_v1_todo_destroy,
  slice: toDOListsSlice
}
