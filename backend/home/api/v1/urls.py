from django.urls import path, include
from rest_framework.routers import DefaultRouter

from home.api.v1.viewsets import (
    SignupViewSet,
    LoginViewSet,
    EditUserView,
    UserProfilePicUpdateView,
    FeedbackViewSet,
    AppointmentViewSet,
    UserProfileViewSet,
    SignUpWithEmailView,
    SendPasswordResetEmailView,
    ChangePasswordView,
    DoctorViewSet,
    ToDoListViewSet,
    ResetPasswordView,
)

router = DefaultRouter()
router.register("signup", SignupViewSet, basename="signup")
router.register("login", LoginViewSet, basename="login")
router.register("feedback", FeedbackViewSet, basename="feedback")
router.register(r'user-profiles', UserProfileViewSet, basename='user-profiles')
router.register(r'doctors', DoctorViewSet, basename='doctors')
router.register(r'todo', ToDoListViewSet, basename='todo-list')

urlpatterns = [
    path("", include(router.urls)),
    path('update-profile-pic/<int:pk>/', UserProfilePicUpdateView.as_view(), name='update-profile-pic'),
    path('signup-with-email/', SignUpWithEmailView.as_view(), name='signup-with-email'),
    path('edit-user/<int:pk>/', EditUserView.as_view(), name='edit-user'),
    path('sendresetpasswordemail/', SendPasswordResetEmailView.as_view(), name='sendresetpasswordemail'),
    path('changepassword/',ChangePasswordView.as_view(), name='changepassword'),
    path('appointments/update-feedback/', AppointmentViewSet.as_view({'patch': 'update_feedback'}), name='update_feedback'),
    path('appointments/create/', AppointmentViewSet.as_view({'post':'create'}), name='create_appointment'),
    path('appointments/', AppointmentViewSet.as_view({'get':'list'}), name='list_appointments'),
    path('appointments/<int:pk>/', AppointmentViewSet.as_view({'get':'retrieve'}), name='get_appointment'),    
    path('appointments/todo_appointments/<int:user_id>/', AppointmentViewSet.as_view({'get': 'todo_appointments'}), name='todo_appointments'),
    path('doctors/<int:pk>/favourite/', DoctorViewSet.as_view({'post': 'favourite'}), name='favourite'),
    path('resetpassword/',ResetPasswordView.as_view(), name='resetpassword'),
]
