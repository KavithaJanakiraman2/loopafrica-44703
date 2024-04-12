import axios from "axios"
const silentseaAPI = axios.create({
  baseURL: "https://loopafrica-44703.botics.co",
  headers: { Accept: "application/json", "Content-Type": "application/json" }
})
function api_docs_schema_retrieve(payload) {
  return silentseaAPI.get(`/api-docs/schema/`, {
    params: { lang: payload.lang }
  })
}
function api_v1_appointments_list(payload) {
  return silentseaAPI.get(`/api/v1/appointments/`)
}
function api_v1_appointments_retrieve(payload) {
  return silentseaAPI.get(`/api/v1/appointments/${payload.id}/`)
}
function api_v1_appointments_create_create(payload) {
  return silentseaAPI.post(`/api/v1/appointments/create/`, payload)
}
function api_v1_appointments_todo_appointments_retrieve(payload) {
  return silentseaAPI.get(
    `/api/v1/appointments/todo_appointments/${payload.user_id}/`
  )
}
function api_v1_appointments_update_feedback_partial_update(payload) {
  return silentseaAPI.patch(`/api/v1/appointments/update-feedback/`, payload)
}
function api_v1_changepassword_create(payload) {
  return silentseaAPI.post(`/api/v1/changepassword/`)
}
function api_v1_doctors_list(payload) {
  return silentseaAPI.get(`/api/v1/doctors/`, {
    params: {
      limit: payload.limit,
      offset: payload.offset,
      ordering: payload.ordering,
      search: payload.search
    }
  })
}
function api_v1_doctors_create(payload) {
  return silentseaAPI.post(`/api/v1/doctors/`, payload)
}
function api_v1_doctors_retrieve(payload) {
  return silentseaAPI.get(`/api/v1/doctors/${payload.id}/`)
}
function api_v1_doctors_update(payload) {
  return silentseaAPI.put(`/api/v1/doctors/${payload.id}/`, payload)
}
function api_v1_doctors_partial_update(payload) {
  return silentseaAPI.patch(`/api/v1/doctors/${payload.id}/`, payload)
}
function api_v1_doctors_destroy(payload) {
  return silentseaAPI.delete(`/api/v1/doctors/${payload.id}/`)
}
function api_v1_doctors_favourite_create_2(payload) {
  return silentseaAPI.post(`/api/v1/doctors/${payload.id}/favourite/`, payload)
}
function api_v1_doctors_doctor_specialized_retrieve(payload) {
  return silentseaAPI.get(`/api/v1/doctors/doctor_specialized/`)
}
function api_v1_doctors_favourite_retrieve(payload) {
  return silentseaAPI.get(`/api/v1/doctors/favourite/`)
}
function api_v1_doctors_favourite_create(payload) {
  return silentseaAPI.post(`/api/v1/doctors/favourite/`, payload)
}
function api_v1_doctors_patient_count_retrieve(payload) {
  return silentseaAPI.get(`/api/v1/doctors/patient_count/`)
}
function api_v1_edit_user_retrieve(payload) {
  return silentseaAPI.get(`/api/v1/edit-user/${payload.id}/`)
}
function api_v1_edit_user_update(payload) {
  return silentseaAPI.put(`/api/v1/edit-user/${payload.id}/`, payload)
}
function api_v1_edit_user_partial_update(payload) {
  return silentseaAPI.patch(`/api/v1/edit-user/${payload.id}/`, payload)
}
function api_v1_feedback_list(payload) {
  return silentseaAPI.get(`/api/v1/feedback/`)
}
function api_v1_feedback_create(payload) {
  return silentseaAPI.post(`/api/v1/feedback/`, payload)
}
function api_v1_feedback_retrieve(payload) {
  return silentseaAPI.get(`/api/v1/feedback/${payload.id}/`)
}
function api_v1_feedback_update(payload) {
  return silentseaAPI.put(`/api/v1/feedback/${payload.id}/`, payload)
}
function api_v1_feedback_partial_update(payload) {
  return silentseaAPI.patch(`/api/v1/feedback/${payload.id}/`, payload)
}
function api_v1_feedback_destroy(payload) {
  return silentseaAPI.delete(`/api/v1/feedback/${payload.id}/`)
}
function api_v1_login_create(payload) {
  return silentseaAPI.post(`/api/v1/login/`, payload)
}
function api_v1_sendresetpasswordemail_create(payload) {
  return silentseaAPI.post(`/api/v1/sendresetpasswordemail/`)
}
function api_v1_signup_create(payload) {
  return silentseaAPI.post(`/api/v1/signup/`, payload)
}
function api_v1_signup_with_email_create(payload) {
  return silentseaAPI.post(`/api/v1/signup-with-email/`, payload)
}
function api_v1_todo_list(payload) {
  return silentseaAPI.get(`/api/v1/todo/`)
}
function api_v1_todo_create(payload) {
  return silentseaAPI.post(`/api/v1/todo/`, payload)
}
function api_v1_todo_retrieve(payload) {
  return silentseaAPI.get(`/api/v1/todo/${payload.id}/`)
}
function api_v1_todo_update(payload) {
  return silentseaAPI.put(`/api/v1/todo/${payload.id}/`, payload)
}
function api_v1_todo_partial_update(payload) {
  return silentseaAPI.patch(`/api/v1/todo/${payload.id}/`, payload)
}
function api_v1_todo_destroy(payload) {
  return silentseaAPI.delete(`/api/v1/todo/${payload.id}/`)
}
function api_v1_todo_delete_completed_destroy(payload) {
  return silentseaAPI.delete(`/api/v1/todo/delete_completed/`)
}
function api_v1_update_profile_pic_retrieve(payload) {
  return silentseaAPI.get(`/api/v1/update-profile-pic/${payload.id}/`)
}
function api_v1_update_profile_pic_update(payload) {
  return silentseaAPI.put(`/api/v1/update-profile-pic/${payload.id}/`, payload)
}
function api_v1_update_profile_pic_partial_update(payload) {
  return silentseaAPI.patch(
    `/api/v1/update-profile-pic/${payload.id}/`,
    payload
  )
}
function api_v1_user_profiles_list(payload) {
  return silentseaAPI.get(`/api/v1/user-profiles/`)
}
function api_v1_user_profiles_create(payload) {
  return silentseaAPI.post(`/api/v1/user-profiles/`, payload)
}
function api_v1_user_profiles_retrieve(payload) {
  return silentseaAPI.get(`/api/v1/user-profiles/${payload.id}/`)
}
function api_v1_user_profiles_update(payload) {
  return silentseaAPI.put(`/api/v1/user-profiles/${payload.id}/`, payload)
}
function api_v1_user_profiles_partial_update(payload) {
  return silentseaAPI.patch(`/api/v1/user-profiles/${payload.id}/`, payload)
}
function api_v1_user_profiles_destroy(payload) {
  return silentseaAPI.delete(`/api/v1/user-profiles/${payload.id}/`)
}
function api_v1_user_profiles_profile_retrieve(payload) {
  return silentseaAPI.get(`/api/v1/user-profiles/profile/`)
}
function api_v1_user_profiles_profile_completion_retrieve(payload) {
  return silentseaAPI.get(`/api/v1/user-profiles/profile_completion/`)
}
function api_v1_user_profiles_update_profile_create(payload) {
  return silentseaAPI.post(`/api/v1/user-profiles/update_profile/`, payload)
}
function modules_contact_us_contact_us_create(payload) {
  return silentseaAPI.post(`/modules/contact-us/contact_us/`)
}
function modules_inventory_management_category_list(payload) {
  return silentseaAPI.get(`/modules/inventory-management/category/`)
}
function modules_inventory_management_category_create(payload) {
  return silentseaAPI.post(`/modules/inventory-management/category/`, payload)
}
function modules_inventory_management_category_retrieve(payload) {
  return silentseaAPI.get(
    `/modules/inventory-management/category/${payload.id}/`
  )
}
function modules_inventory_management_category_update(payload) {
  return silentseaAPI.put(
    `/modules/inventory-management/category/${payload.id}/`,
    payload
  )
}
function modules_inventory_management_category_partial_update(payload) {
  return silentseaAPI.patch(
    `/modules/inventory-management/category/${payload.id}/`,
    payload
  )
}
function modules_inventory_management_category_destroy(payload) {
  return silentseaAPI.delete(
    `/modules/inventory-management/category/${payload.id}/`
  )
}
function modules_inventory_management_invoice_list(payload) {
  return silentseaAPI.get(`/modules/inventory-management/invoice/`)
}
function modules_inventory_management_invoice_create(payload) {
  return silentseaAPI.post(`/modules/inventory-management/invoice/`, payload)
}
function modules_inventory_management_invoice_item_list(payload) {
  return silentseaAPI.get(`/modules/inventory-management/invoice-item/`)
}
function modules_inventory_management_invoice_item_create(payload) {
  return silentseaAPI.post(
    `/modules/inventory-management/invoice-item/`,
    payload
  )
}
function modules_inventory_management_invoice_item_retrieve(payload) {
  return silentseaAPI.get(
    `/modules/inventory-management/invoice-item/${payload.id}/`
  )
}
function modules_inventory_management_invoice_item_update(payload) {
  return silentseaAPI.put(
    `/modules/inventory-management/invoice-item/${payload.id}/`,
    payload
  )
}
function modules_inventory_management_invoice_item_partial_update(payload) {
  return silentseaAPI.patch(
    `/modules/inventory-management/invoice-item/${payload.id}/`,
    payload
  )
}
function modules_inventory_management_invoice_item_destroy(payload) {
  return silentseaAPI.delete(
    `/modules/inventory-management/invoice-item/${payload.id}/`
  )
}
function modules_inventory_management_invoice_retrieve(payload) {
  return silentseaAPI.get(
    `/modules/inventory-management/invoice/${payload.id}/`
  )
}
function modules_inventory_management_invoice_update(payload) {
  return silentseaAPI.put(
    `/modules/inventory-management/invoice/${payload.id}/`,
    payload
  )
}
function modules_inventory_management_invoice_partial_update(payload) {
  return silentseaAPI.patch(
    `/modules/inventory-management/invoice/${payload.id}/`,
    payload
  )
}
function modules_inventory_management_invoice_destroy(payload) {
  return silentseaAPI.delete(
    `/modules/inventory-management/invoice/${payload.id}/`
  )
}
function modules_inventory_management_product_list(payload) {
  return silentseaAPI.get(`/modules/inventory-management/product/`)
}
function modules_inventory_management_product_create(payload) {
  return silentseaAPI.post(`/modules/inventory-management/product/`, payload)
}
function modules_inventory_management_product_retrieve(payload) {
  return silentseaAPI.get(
    `/modules/inventory-management/product/${payload.id}/`
  )
}
function modules_inventory_management_product_update(payload) {
  return silentseaAPI.put(
    `/modules/inventory-management/product/${payload.id}/`,
    payload
  )
}
function modules_inventory_management_product_partial_update(payload) {
  return silentseaAPI.patch(
    `/modules/inventory-management/product/${payload.id}/`,
    payload
  )
}
function modules_inventory_management_product_destroy(payload) {
  return silentseaAPI.delete(
    `/modules/inventory-management/product/${payload.id}/`
  )
}
function modules_inventory_management_stock_list(payload) {
  return silentseaAPI.get(`/modules/inventory-management/stock/`)
}
function modules_inventory_management_stock_create(payload) {
  return silentseaAPI.post(`/modules/inventory-management/stock/`, payload)
}
function modules_inventory_management_stock_retrieve(payload) {
  return silentseaAPI.get(`/modules/inventory-management/stock/${payload.id}/`)
}
function modules_inventory_management_stock_update(payload) {
  return silentseaAPI.put(
    `/modules/inventory-management/stock/${payload.id}/`,
    payload
  )
}
function modules_inventory_management_stock_partial_update(payload) {
  return silentseaAPI.patch(
    `/modules/inventory-management/stock/${payload.id}/`,
    payload
  )
}
function modules_inventory_management_stock_destroy(payload) {
  return silentseaAPI.delete(
    `/modules/inventory-management/stock/${payload.id}/`
  )
}
function modules_inventory_management_supplier_list(payload) {
  return silentseaAPI.get(`/modules/inventory-management/supplier/`)
}
function modules_inventory_management_supplier_create(payload) {
  return silentseaAPI.post(`/modules/inventory-management/supplier/`, payload)
}
function modules_inventory_management_supplier_retrieve(payload) {
  return silentseaAPI.get(
    `/modules/inventory-management/supplier/${payload.id}/`
  )
}
function modules_inventory_management_supplier_update(payload) {
  return silentseaAPI.put(
    `/modules/inventory-management/supplier/${payload.id}/`,
    payload
  )
}
function modules_inventory_management_supplier_partial_update(payload) {
  return silentseaAPI.patch(
    `/modules/inventory-management/supplier/${payload.id}/`,
    payload
  )
}
function modules_inventory_management_supplier_destroy(payload) {
  return silentseaAPI.delete(
    `/modules/inventory-management/supplier/${payload.id}/`
  )
}
function modules_privacy_policy_list(payload) {
  return silentseaAPI.get(`/modules/privacy-policy/`)
}
function modules_privacy_policy_create(payload) {
  return silentseaAPI.post(`/modules/privacy-policy/`, payload)
}
function modules_privacy_policy_retrieve(payload) {
  return silentseaAPI.get(`/modules/privacy-policy/${payload.id}/`)
}
function modules_privacy_policy_update(payload) {
  return silentseaAPI.put(`/modules/privacy-policy/${payload.id}/`, payload)
}
function modules_privacy_policy_partial_update(payload) {
  return silentseaAPI.patch(`/modules/privacy-policy/${payload.id}/`, payload)
}
function modules_privacy_policy_destroy(payload) {
  return silentseaAPI.delete(`/modules/privacy-policy/${payload.id}/`)
}
function modules_push_notifications_notifications_list(payload) {
  return silentseaAPI.get(`/modules/push-notifications/notifications/`)
}
function modules_push_notifications_notifications_create(payload) {
  return silentseaAPI.post(
    `/modules/push-notifications/notifications/`,
    payload
  )
}
function modules_push_notifications_notifications_retrieve(payload) {
  return silentseaAPI.get(
    `/modules/push-notifications/notifications/${payload.id}/`
  )
}
function modules_push_notifications_notifications_destroy(payload) {
  return silentseaAPI.delete(
    `/modules/push-notifications/notifications/${payload.id}/`
  )
}
function modules_terms_and_conditions_list(payload) {
  return silentseaAPI.get(`/modules/terms-and-conditions/`)
}
function modules_terms_and_conditions_create(payload) {
  return silentseaAPI.post(`/modules/terms-and-conditions/`, payload)
}
function modules_terms_and_conditions_retrieve(payload) {
  return silentseaAPI.get(`/modules/terms-and-conditions/${payload.id}/`)
}
function modules_terms_and_conditions_update(payload) {
  return silentseaAPI.put(
    `/modules/terms-and-conditions/${payload.id}/`,
    payload
  )
}
function modules_terms_and_conditions_partial_update(payload) {
  return silentseaAPI.patch(
    `/modules/terms-and-conditions/${payload.id}/`,
    payload
  )
}
function modules_terms_and_conditions_destroy(payload) {
  return silentseaAPI.delete(`/modules/terms-and-conditions/${payload.id}/`)
}
function modules_twofactorauth_send_otp_create(payload) {
  return silentseaAPI.post(`/modules/twofactorauth/send-otp/`, payload)
}
function modules_twofactorauth_verify_delete_destroy(payload) {
  return silentseaAPI.delete(`/modules/twofactorauth/verify-delete/`)
}
function patient_medical_records_list(payload) {
  return silentseaAPI.get(`/patient/medical_records/`)
}
function patient_medical_records_create(payload) {
  return silentseaAPI.post(`/patient/medical_records/`, payload)
}
function patient_medical_records_retrieve(payload) {
  return silentseaAPI.get(`/patient/medical_records/${payload.id}/`)
}
function patient_medical_records_update(payload) {
  return silentseaAPI.put(`/patient/medical_records/${payload.id}/`, payload)
}
function patient_medical_records_partial_update(payload) {
  return silentseaAPI.patch(`/patient/medical_records/${payload.id}/`, payload)
}
function patient_medical_records_destroy(payload) {
  return silentseaAPI.delete(`/patient/medical_records/${payload.id}/`)
}
function patient_patient_list(payload) {
  return silentseaAPI.get(`/patient/patient/`)
}
function patient_patient_create(payload) {
  return silentseaAPI.post(`/patient/patient/`, payload)
}
function patient_patient_retrieve(payload) {
  return silentseaAPI.get(`/patient/patient/${payload.id}/`)
}
function patient_patient_update(payload) {
  return silentseaAPI.put(`/patient/patient/${payload.id}/`, payload)
}
function patient_patient_partial_update(payload) {
  return silentseaAPI.patch(`/patient/patient/${payload.id}/`, payload)
}
function patient_patient_destroy(payload) {
  return silentseaAPI.delete(`/patient/patient/${payload.id}/`)
}
function patient_prescriptions_list(payload) {
  return silentseaAPI.get(`/patient/prescriptions/`)
}
function patient_prescriptions_create(payload) {
  return silentseaAPI.post(`/patient/prescriptions/`, payload)
}
function patient_prescriptions_retrieve(payload) {
  return silentseaAPI.get(`/patient/prescriptions/${payload.id}/`)
}
function patient_prescriptions_update(payload) {
  return silentseaAPI.put(`/patient/prescriptions/${payload.id}/`, payload)
}
function patient_prescriptions_partial_update(payload) {
  return silentseaAPI.patch(`/patient/prescriptions/${payload.id}/`, payload)
}
function patient_prescriptions_destroy(payload) {
  return silentseaAPI.delete(`/patient/prescriptions/${payload.id}/`)
}
function patient_prescriptions_medicationlist_retrieve(payload) {
  return silentseaAPI.get(`/patient/prescriptions/medicationlist/`)
}
function patient_prescriptions_medicationlist_retrieve_2(payload) {
  return silentseaAPI.get(
    `/patient/prescriptions/medicationlist/${payload.user_id}/`
  )
}
function patient_prescriptions_todo_medication_retrieve(payload) {
  return silentseaAPI.get(`/patient/prescriptions/todo_medication/`)
}
function patient_prescriptions_todo_medication_retrieve_2(payload) {
  return silentseaAPI.get(
    `/patient/prescriptions/todo_medication/${payload.user_id}/`
  )
}
function patient_test_results_list(payload) {
  return silentseaAPI.get(`/patient/test-results/`)
}
function patient_test_results_create(payload) {
  return silentseaAPI.post(`/patient/test-results/`, payload)
}
function patient_test_results_upload_list(payload) {
  return silentseaAPI.get(`/patient/test-results-upload/`)
}
function patient_test_results_upload_create(payload) {
  return silentseaAPI.post(`/patient/test-results-upload/`, payload)
}
function patient_test_results_upload_retrieve(payload) {
  return silentseaAPI.get(`/patient/test-results-upload/${payload.id}/`)
}
function patient_test_results_upload_update(payload) {
  return silentseaAPI.put(
    `/patient/test-results-upload/${payload.id}/`,
    payload
  )
}
function patient_test_results_upload_partial_update(payload) {
  return silentseaAPI.patch(
    `/patient/test-results-upload/${payload.id}/`,
    payload
  )
}
function patient_test_results_upload_destroy(payload) {
  return silentseaAPI.delete(`/patient/test-results-upload/${payload.id}/`)
}
function patient_test_results_retrieve(payload) {
  return silentseaAPI.get(`/patient/test-results/${payload.id}/`)
}
function patient_test_results_update(payload) {
  return silentseaAPI.put(`/patient/test-results/${payload.id}/`, payload)
}
function patient_test_results_partial_update(payload) {
  return silentseaAPI.patch(`/patient/test-results/${payload.id}/`, payload)
}
function patient_test_results_destroy(payload) {
  return silentseaAPI.delete(`/patient/test-results/${payload.id}/`)
}
function patient_vitals_list(payload) {
  return silentseaAPI.get(`/patient/vitals/`)
}
function patient_vitals_create(payload) {
  return silentseaAPI.post(`/patient/vitals/`, payload)
}
function patient_vitals_retrieve(payload) {
  return silentseaAPI.get(`/patient/vitals/${payload.id}/`)
}
function patient_vitals_update(payload) {
  return silentseaAPI.put(`/patient/vitals/${payload.id}/`, payload)
}
function patient_vitals_partial_update(payload) {
  return silentseaAPI.patch(`/patient/vitals/${payload.id}/`, payload)
}
function patient_vitals_destroy(payload) {
  return silentseaAPI.delete(`/patient/vitals/${payload.id}/`)
}
function rest_auth_login_create(payload) {
  return silentseaAPI.post(`/rest-auth/login/`, payload)
}
function rest_auth_logout_retrieve(payload) {
  return silentseaAPI.get(`/rest-auth/logout/`)
}
function rest_auth_logout_create(payload) {
  return silentseaAPI.post(`/rest-auth/logout/`)
}
function rest_auth_password_change_create(payload) {
  return silentseaAPI.post(`/rest-auth/password/change/`, payload)
}
function rest_auth_password_reset_create(payload) {
  return silentseaAPI.post(`/rest-auth/password/reset/`, payload)
}
function rest_auth_password_reset_confirm_create(payload) {
  return silentseaAPI.post(`/rest-auth/password/reset/confirm/`, payload)
}
function rest_auth_registration_create(payload) {
  return silentseaAPI.post(`/rest-auth/registration/`, payload)
}
function rest_auth_registration_verify_email_create(payload) {
  return silentseaAPI.post(`/rest-auth/registration/verify-email/`, payload)
}
function rest_auth_user_retrieve(payload) {
  return silentseaAPI.get(`/rest-auth/user/`)
}
function rest_auth_user_update(payload) {
  return silentseaAPI.put(`/rest-auth/user/`, payload)
}
function rest_auth_user_partial_update(payload) {
  return silentseaAPI.patch(`/rest-auth/user/`, payload)
}
export const apiService = {
  api_docs_schema_retrieve,
  api_v1_appointments_list,
  api_v1_appointments_retrieve,
  api_v1_appointments_create_create,
  api_v1_appointments_todo_appointments_retrieve,
  api_v1_appointments_update_feedback_partial_update,
  api_v1_changepassword_create,
  api_v1_doctors_list,
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
  api_v1_edit_user_retrieve,
  api_v1_edit_user_update,
  api_v1_edit_user_partial_update,
  api_v1_feedback_list,
  api_v1_feedback_create,
  api_v1_feedback_retrieve,
  api_v1_feedback_update,
  api_v1_feedback_partial_update,
  api_v1_feedback_destroy,
  api_v1_login_create,
  api_v1_sendresetpasswordemail_create,
  api_v1_signup_create,
  api_v1_signup_with_email_create,
  api_v1_todo_list,
  api_v1_todo_create,
  api_v1_todo_retrieve,
  api_v1_todo_update,
  api_v1_todo_partial_update,
  api_v1_todo_destroy,
  api_v1_todo_delete_completed_destroy,
  api_v1_update_profile_pic_retrieve,
  api_v1_update_profile_pic_update,
  api_v1_update_profile_pic_partial_update,
  api_v1_user_profiles_list,
  api_v1_user_profiles_create,
  api_v1_user_profiles_retrieve,
  api_v1_user_profiles_update,
  api_v1_user_profiles_partial_update,
  api_v1_user_profiles_destroy,
  api_v1_user_profiles_profile_retrieve,
  api_v1_user_profiles_profile_completion_retrieve,
  api_v1_user_profiles_update_profile_create,
  modules_contact_us_contact_us_create,
  modules_inventory_management_category_list,
  modules_inventory_management_category_create,
  modules_inventory_management_category_retrieve,
  modules_inventory_management_category_update,
  modules_inventory_management_category_partial_update,
  modules_inventory_management_category_destroy,
  modules_inventory_management_invoice_list,
  modules_inventory_management_invoice_create,
  modules_inventory_management_invoice_item_list,
  modules_inventory_management_invoice_item_create,
  modules_inventory_management_invoice_item_retrieve,
  modules_inventory_management_invoice_item_update,
  modules_inventory_management_invoice_item_partial_update,
  modules_inventory_management_invoice_item_destroy,
  modules_inventory_management_invoice_retrieve,
  modules_inventory_management_invoice_update,
  modules_inventory_management_invoice_partial_update,
  modules_inventory_management_invoice_destroy,
  modules_inventory_management_product_list,
  modules_inventory_management_product_create,
  modules_inventory_management_product_retrieve,
  modules_inventory_management_product_update,
  modules_inventory_management_product_partial_update,
  modules_inventory_management_product_destroy,
  modules_inventory_management_stock_list,
  modules_inventory_management_stock_create,
  modules_inventory_management_stock_retrieve,
  modules_inventory_management_stock_update,
  modules_inventory_management_stock_partial_update,
  modules_inventory_management_stock_destroy,
  modules_inventory_management_supplier_list,
  modules_inventory_management_supplier_create,
  modules_inventory_management_supplier_retrieve,
  modules_inventory_management_supplier_update,
  modules_inventory_management_supplier_partial_update,
  modules_inventory_management_supplier_destroy,
  modules_privacy_policy_list,
  modules_privacy_policy_create,
  modules_privacy_policy_retrieve,
  modules_privacy_policy_update,
  modules_privacy_policy_partial_update,
  modules_privacy_policy_destroy,
  modules_push_notifications_notifications_list,
  modules_push_notifications_notifications_create,
  modules_push_notifications_notifications_retrieve,
  modules_push_notifications_notifications_destroy,
  modules_terms_and_conditions_list,
  modules_terms_and_conditions_create,
  modules_terms_and_conditions_retrieve,
  modules_terms_and_conditions_update,
  modules_terms_and_conditions_partial_update,
  modules_terms_and_conditions_destroy,
  modules_twofactorauth_send_otp_create,
  modules_twofactorauth_verify_delete_destroy,
  patient_medical_records_list,
  patient_medical_records_create,
  patient_medical_records_retrieve,
  patient_medical_records_update,
  patient_medical_records_partial_update,
  patient_medical_records_destroy,
  patient_patient_list,
  patient_patient_create,
  patient_patient_retrieve,
  patient_patient_update,
  patient_patient_partial_update,
  patient_patient_destroy,
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
  patient_test_results_list,
  patient_test_results_create,
  patient_test_results_upload_list,
  patient_test_results_upload_create,
  patient_test_results_upload_retrieve,
  patient_test_results_upload_update,
  patient_test_results_upload_partial_update,
  patient_test_results_upload_destroy,
  patient_test_results_retrieve,
  patient_test_results_update,
  patient_test_results_partial_update,
  patient_test_results_destroy,
  patient_vitals_list,
  patient_vitals_create,
  patient_vitals_retrieve,
  patient_vitals_update,
  patient_vitals_partial_update,
  patient_vitals_destroy,
  rest_auth_login_create,
  rest_auth_logout_retrieve,
  rest_auth_logout_create,
  rest_auth_password_change_create,
  rest_auth_password_reset_create,
  rest_auth_password_reset_confirm_create,
  rest_auth_registration_create,
  rest_auth_registration_verify_email_create,
  rest_auth_user_retrieve,
  rest_auth_user_update,
  rest_auth_user_partial_update
}
