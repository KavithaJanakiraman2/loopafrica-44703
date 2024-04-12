import { createSlice, createAsyncThunk } from "@reduxjs/toolkit"
import { apiService } from "./api"
export const patient_prescriptions_list = createAsyncThunk(
  "prescriptions/patient_prescriptions_list",
  async payload => {
    const response = await apiService.patient_prescriptions_list(payload)
    return response.data
  }
)
export const patient_prescriptions_create = createAsyncThunk(
  "prescriptions/patient_prescriptions_create",
  async payload => {
    const response = await apiService.patient_prescriptions_create(payload)
    return response.data
  }
)
export const patient_prescriptions_retrieve = createAsyncThunk(
  "prescriptions/patient_prescriptions_retrieve",
  async payload => {
    const response = await apiService.patient_prescriptions_retrieve(payload)
    return response.data
  }
)
export const patient_prescriptions_update = createAsyncThunk(
  "prescriptions/patient_prescriptions_update",
  async payload => {
    const response = await apiService.patient_prescriptions_update(payload)
    return response.data
  }
)
export const patient_prescriptions_partial_update = createAsyncThunk(
  "prescriptions/patient_prescriptions_partial_update",
  async payload => {
    const response = await apiService.patient_prescriptions_partial_update(
      payload
    )
    return response.data
  }
)
export const patient_prescriptions_destroy = createAsyncThunk(
  "prescriptions/patient_prescriptions_destroy",
  async payload => {
    const response = await apiService.patient_prescriptions_destroy(payload)
    return response.data
  }
)
export const patient_prescriptions_medicationlist_retrieve = createAsyncThunk(
  "prescriptions/patient_prescriptions_medicationlist_retrieve",
  async payload => {
    const response = await apiService.patient_prescriptions_medicationlist_retrieve(
      payload
    )
    return response.data
  }
)
export const patient_prescriptions_medicationlist_retrieve_2 = createAsyncThunk(
  "prescriptions/patient_prescriptions_medicationlist_retrieve_2",
  async payload => {
    const response = await apiService.patient_prescriptions_medicationlist_retrieve_2(
      payload
    )
    return response.data
  }
)
export const patient_prescriptions_todo_medication_retrieve = createAsyncThunk(
  "prescriptions/patient_prescriptions_todo_medication_retrieve",
  async payload => {
    const response = await apiService.patient_prescriptions_todo_medication_retrieve(
      payload
    )
    return response.data
  }
)
export const patient_prescriptions_todo_medication_retrieve_2 = createAsyncThunk(
  "prescriptions/patient_prescriptions_todo_medication_retrieve_2",
  async payload => {
    const response = await apiService.patient_prescriptions_todo_medication_retrieve_2(
      payload
    )
    return response.data
  }
)
const initialState = { entities: [], api: { loading: "idle", error: null } }
const prescriptionsSlice = createSlice({
  name: "prescriptions",
  initialState,
  reducers: {},
  extraReducers: builder => {
    builder
      .addCase(patient_prescriptions_list.pending, (state, action) => {
        if (state.api.loading === "idle") {
          state.api.loading = "pending"
        }
      })
      .addCase(patient_prescriptions_list.fulfilled, (state, action) => {
        if (state.api.loading === "pending") {
          state.entities = action.payload
          state.api.loading = "idle"
        }
      })
      .addCase(patient_prescriptions_list.rejected, (state, action) => {
        if (state.api.loading === "pending") {
          state.api.error = action.error
          state.api.loading = "idle"
        }
      })
      .addCase(patient_prescriptions_create.pending, (state, action) => {
        if (state.api.loading === "idle") {
          state.api.loading = "pending"
        }
      })
      .addCase(patient_prescriptions_create.fulfilled, (state, action) => {
        if (state.api.loading === "pending") {
          state.entities.push(action.payload)
          state.api.loading = "idle"
        }
      })
      .addCase(patient_prescriptions_create.rejected, (state, action) => {
        if (state.api.loading === "pending") {
          state.api.error = action.error
          state.api.loading = "idle"
        }
      })
      .addCase(patient_prescriptions_retrieve.pending, (state, action) => {
        if (state.api.loading === "idle") {
          state.api.loading = "pending"
        }
      })
      .addCase(patient_prescriptions_retrieve.fulfilled, (state, action) => {
        if (state.api.loading === "pending") {
          state.entities = [
            ...state.entities.filter(record => record.id !== action.payload.id),
            action.payload
          ]
          state.api.loading = "idle"
        }
      })
      .addCase(patient_prescriptions_retrieve.rejected, (state, action) => {
        if (state.api.loading === "pending") {
          state.api.error = action.error
          state.api.loading = "idle"
        }
      })
      .addCase(patient_prescriptions_update.pending, (state, action) => {
        if (state.api.loading === "idle") {
          state.api.loading = "pending"
        }
      })
      .addCase(patient_prescriptions_update.fulfilled, (state, action) => {
        if (state.api.loading === "pending") {
          state.entities = state.entities.map(record =>
            record.id === action.payload.id ? action.payload : record
          )
          state.api.loading = "idle"
        }
      })
      .addCase(patient_prescriptions_update.rejected, (state, action) => {
        if (state.api.loading === "pending") {
          state.api.error = action.error
          state.api.loading = "idle"
        }
      })
      .addCase(
        patient_prescriptions_partial_update.pending,
        (state, action) => {
          if (state.api.loading === "idle") {
            state.api.loading = "pending"
          }
        }
      )
      .addCase(
        patient_prescriptions_partial_update.fulfilled,
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
        patient_prescriptions_partial_update.rejected,
        (state, action) => {
          if (state.api.loading === "pending") {
            state.api.error = action.error
            state.api.loading = "idle"
          }
        }
      )
      .addCase(patient_prescriptions_destroy.pending, (state, action) => {
        if (state.api.loading === "idle") {
          state.api.loading = "pending"
        }
      })
      .addCase(patient_prescriptions_destroy.fulfilled, (state, action) => {
        if (state.api.loading === "pending") {
          state.entities = state.entities.filter(
            record => record.id !== action.meta.arg?.id
          )
          state.api.loading = "idle"
        }
      })
      .addCase(patient_prescriptions_destroy.rejected, (state, action) => {
        if (state.api.loading === "pending") {
          state.api.error = action.error
          state.api.loading = "idle"
        }
      })
      .addCase(
        patient_prescriptions_medicationlist_retrieve.pending,
        (state, action) => {
          if (state.api.loading === "idle") {
            state.api.loading = "pending"
          }
        }
      )
      .addCase(
        patient_prescriptions_medicationlist_retrieve.fulfilled,
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
        patient_prescriptions_medicationlist_retrieve.rejected,
        (state, action) => {
          if (state.api.loading === "pending") {
            state.api.error = action.error
            state.api.loading = "idle"
          }
        }
      )
      .addCase(
        patient_prescriptions_medicationlist_retrieve_2.pending,
        (state, action) => {
          if (state.api.loading === "idle") {
            state.api.loading = "pending"
          }
        }
      )
      .addCase(
        patient_prescriptions_medicationlist_retrieve_2.fulfilled,
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
        patient_prescriptions_medicationlist_retrieve_2.rejected,
        (state, action) => {
          if (state.api.loading === "pending") {
            state.api.error = action.error
            state.api.loading = "idle"
          }
        }
      )
      .addCase(
        patient_prescriptions_todo_medication_retrieve.pending,
        (state, action) => {
          if (state.api.loading === "idle") {
            state.api.loading = "pending"
          }
        }
      )
      .addCase(
        patient_prescriptions_todo_medication_retrieve.fulfilled,
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
        patient_prescriptions_todo_medication_retrieve.rejected,
        (state, action) => {
          if (state.api.loading === "pending") {
            state.api.error = action.error
            state.api.loading = "idle"
          }
        }
      )
      .addCase(
        patient_prescriptions_todo_medication_retrieve_2.pending,
        (state, action) => {
          if (state.api.loading === "idle") {
            state.api.loading = "pending"
          }
        }
      )
      .addCase(
        patient_prescriptions_todo_medication_retrieve_2.fulfilled,
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
        patient_prescriptions_todo_medication_retrieve_2.rejected,
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
  patient_prescriptions_list,
  patient_prescriptions_create,
  patient_prescriptions_retrieve,
  patient_prescriptions_update,
  patient_prescriptions_partial_update,
  patient_prescriptions_destroy,
  patient_prescriptions_medicationlist_retrieve,
  patient_prescriptions_medicationlist_retrieve_2,
  patient_prescriptions_todo_medication_retrieve,
  patient_prescriptions_todo_medication_retrieve_2,
  slice: prescriptionsSlice
}
