from django.urls import path, include
from rest_framework.routers import DefaultRouter
#from .views import VitalsViewSet
from .viewsets import VitalsViewSet, PrescriptionViewSet, MedicalRecordViewSet, TestResultViewSet, TestResultUploadViewSet

app_name = 'patient_profile'
 
router = DefaultRouter()
router.register(r'vitals', VitalsViewSet)
router.register(r'prescriptions', PrescriptionViewSet)
router.register(r'medical_records', MedicalRecordViewSet)
router.register(r'test-results', TestResultViewSet)
router.register(r'test-results-upload', TestResultUploadViewSet, basename='test-result-upload')

urlpatterns = [
    path('', include(router.urls)),    
    path('prescriptions/medicationlist/<int:user_id>/', PrescriptionViewSet.as_view({'get': 'medicationlist'}), name='medicationlist'),
    path('prescriptions/todo_medication/<int:user_id>/', PrescriptionViewSet.as_view({'get': 'todo_medication'}), name='todo_medication'),
]
