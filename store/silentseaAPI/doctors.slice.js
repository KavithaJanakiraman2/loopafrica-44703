import { createSlice, createAsyncThunk } from "@reduxjs/toolkit"
import { apiService } from "./api"
export const api_v1_doctors_create = createAsyncThunk(
  "doctors/api_v1_doctors_create",
  async payload => {
    const response = await apiService.api_v1_doctors_create(payload)
    return response.data
  }
)
export const api_v1_doctors_retrieve = createAsyncThunk(
  "doctors/api_v1_doctors_retrieve",
  async payload => {
    const response = await apiService.api_v1_doctors_retrieve(payload)
    return response.data
  }
)
export const api_v1_doctors_update = createAsyncThunk(
  "doctors/api_v1_doctors_update",
  async payload => {
    const response = await apiService.api_v1_doctors_update(payload)
    return response.data
  }
)
export const api_v1_doctors_partial_update = createAsyncThunk(
  "doctors/api_v1_doctors_partial_update",
  async payload => {
    const response = await apiService.api_v1_doctors_partial_update(payload)
    return response.data
  }
)
export const api_v1_doctors_destroy = createAsyncThunk(
  "doctors/api_v1_doctors_destroy",
  async payload => {
    const response = await apiService.api_v1_doctors_destroy(payload)
    return response.data
  }
)
export const api_v1_doctors_favourite_create_2 = createAsyncThunk(
  "doctors/api_v1_doctors_favourite_create_2",
  async payload => {
    const response = await apiService.api_v1_doctors_favourite_create_2(payload)
    return response.data
  }
)
export const api_v1_doctors_doctor_specialized_retrieve = createAsyncThunk(
  "doctors/api_v1_doctors_doctor_specialized_retrieve",
  async payload => {
    const response = await apiService.api_v1_doctors_doctor_specialized_retrieve(
      payload
    )
    return response.data
  }
)
export const api_v1_doctors_favourite_retrieve = createAsyncThunk(
  "doctors/api_v1_doctors_favourite_retrieve",
  async payload => {
    const response = await apiService.api_v1_doctors_favourite_retrieve(payload)
    return response.data
  }
)
export const api_v1_doctors_favourite_create = createAsyncThunk(
  "doctors/api_v1_doctors_favourite_create",
  async payload => {
    const response = await apiService.api_v1_doctors_favourite_create(payload)
    return response.data
  }
)
export const api_v1_doctors_patient_count_retrieve = createAsyncThunk(
  "doctors/api_v1_doctors_patient_count_retrieve",
  async payload => {
    const response = await apiService.api_v1_doctors_patient_count_retrieve(
      payload
    )
    return response.data
  }
)
const initialState = { entities: [], api: { loading: "idle", error: null } }
const doctorsSlice = createSlice({
  name: "doctors",
  initialState,
  reducers: {},
  extraReducers: builder => {
    builder
      .addCase(api_v1_doctors_create.pending, (state, action) => {
        if (state.api.loading === "idle") {
          state.api.loading = "pending"
        }
      })
      .addCase(api_v1_doctors_create.fulfilled, (state, action) => {
        if (state.api.loading === "pending") {
          state.entities.push(action.payload)
          state.api.loading = "idle"
        }
      })
      .addCase(api_v1_doctors_create.rejected, (state, action) => {
        if (state.api.loading === "pending") {
          state.api.error = action.error
          state.api.loading = "idle"
        }
      })
      .addCase(api_v1_doctors_retrieve.pending, (state, action) => {
        if (state.api.loading === "idle") {
          state.api.loading = "pending"
        }
      })
      .addCase(api_v1_doctors_retrieve.fulfilled, (state, action) => {
        if (state.api.loading === "pending") {
          state.entities = [
            ...state.entities.filter(record => record.id !== action.payload.id),
            action.payload
          ]
          state.api.loading = "idle"
        }
      })
      .addCase(api_v1_doctors_retrieve.rejected, (state, action) => {
        if (state.api.loading === "pending") {
          state.api.error = action.error
          state.api.loading = "idle"
        }
      })
      .addCase(api_v1_doctors_update.pending, (state, action) => {
        if (state.api.loading === "idle") {
          state.api.loading = "pending"
        }
      })
      .addCase(api_v1_doctors_update.fulfilled, (state, action) => {
        if (state.api.loading === "pending") {
          state.entities = state.entities.map(record =>
            record.id === action.payload.id ? action.payload : record
          )
          state.api.loading = "idle"
        }
      })
      .addCase(api_v1_doctors_update.rejected, (state, action) => {
        if (state.api.loading === "pending") {
          state.api.error = action.error
          state.api.loading = "idle"
        }
      })
      .addCase(api_v1_doctors_partial_update.pending, (state, action) => {
        if (state.api.loading === "idle") {
          state.api.loading = "pending"
        }
      })
      .addCase(api_v1_doctors_partial_update.fulfilled, (state, action) => {
        if (state.api.loading === "pending") {
          state.entities = state.entities.map(record =>
            record.id === action.payload.id ? action.payload : record
          )
          state.api.loading = "idle"
        }
      })
      .addCase(api_v1_doctors_partial_update.rejected, (state, action) => {
        if (state.api.loading === "pending") {
          state.api.error = action.error
          state.api.loading = "idle"
        }
      })
      .addCase(api_v1_doctors_destroy.pending, (state, action) => {
        if (state.api.loading === "idle") {
          state.api.loading = "pending"
        }
      })
      .addCase(api_v1_doctors_destroy.fulfilled, (state, action) => {
        if (state.api.loading === "pending") {
          state.entities = state.entities.filter(
            record => record.id !== action.meta.arg?.id
          )
          state.api.loading = "idle"
        }
      })
      .addCase(api_v1_doctors_destroy.rejected, (state, action) => {
        if (state.api.loading === "pending") {
          state.api.error = action.error
          state.api.loading = "idle"
        }
      })
      .addCase(api_v1_doctors_favourite_create_2.pending, (state, action) => {
        if (state.api.loading === "idle") {
          state.api.loading = "pending"
        }
      })
      .addCase(api_v1_doctors_favourite_create_2.fulfilled, (state, action) => {
        if (state.api.loading === "pending") {
          state.entities.push(action.payload)
          state.api.loading = "idle"
        }
      })
      .addCase(api_v1_doctors_favourite_create_2.rejected, (state, action) => {
        if (state.api.loading === "pending") {
          state.api.error = action.error
          state.api.loading = "idle"
        }
      })
      .addCase(
        api_v1_doctors_doctor_specialized_retrieve.pending,
        (state, action) => {
          if (state.api.loading === "idle") {
            state.api.loading = "pending"
          }
        }
      )
      .addCase(
        api_v1_doctors_doctor_specialized_retrieve.fulfilled,
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
        api_v1_doctors_doctor_specialized_retrieve.rejected,
        (state, action) => {
          if (state.api.loading === "pending") {
            state.api.error = action.error
            state.api.loading = "idle"
          }
        }
      )
      .addCase(api_v1_doctors_favourite_retrieve.pending, (state, action) => {
        if (state.api.loading === "idle") {
          state.api.loading = "pending"
        }
      })
      .addCase(api_v1_doctors_favourite_retrieve.fulfilled, (state, action) => {
        if (state.api.loading === "pending") {
          state.entities = [
            ...state.entities.filter(record => record.id !== action.payload.id),
            action.payload
          ]
          state.api.loading = "idle"
        }
      })
      .addCase(api_v1_doctors_favourite_retrieve.rejected, (state, action) => {
        if (state.api.loading === "pending") {
          state.api.error = action.error
          state.api.loading = "idle"
        }
      })
      .addCase(api_v1_doctors_favourite_create.pending, (state, action) => {
        if (state.api.loading === "idle") {
          state.api.loading = "pending"
        }
      })
      .addCase(api_v1_doctors_favourite_create.fulfilled, (state, action) => {
        if (state.api.loading === "pending") {
          state.entities.push(action.payload)
          state.api.loading = "idle"
        }
      })
      .addCase(api_v1_doctors_favourite_create.rejected, (state, action) => {
        if (state.api.loading === "pending") {
          state.api.error = action.error
          state.api.loading = "idle"
        }
      })
      .addCase(
        api_v1_doctors_patient_count_retrieve.pending,
        (state, action) => {
          if (state.api.loading === "idle") {
            state.api.loading = "pending"
          }
        }
      )
      .addCase(
        api_v1_doctors_patient_count_retrieve.fulfilled,
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
        api_v1_doctors_patient_count_retrieve.rejected,
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
  api_v1_doctors_create,
  api_v1_doctors_retrieve,
  api_v1_doctors_update,
  api_v1_doctors_partial_update,
  api_v1_doctors_destroy,
  api_v1_doctors_favourite_create_2,
  api_v1_doctors_doctor_specialized_retrieve,
  api_v1_doctors_favourite_retrieve,
  api_v1_doctors_favourite_create,
  api_v1_doctors_patient_count_retrieve,
  slice: doctorsSlice
}
