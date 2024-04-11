from django.urls import path
from django.contrib.auth.views import PasswordChangeView

from users.views import (
    user_redirect_view,
    user_update_view,
    user_detail_view,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
    path("changepassword/<uidb64>/<token>/", PasswordChangeView.as_view(), name="changepassword"),
]
