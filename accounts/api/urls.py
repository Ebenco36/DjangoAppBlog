from django.conf.urls import url
from django.urls import path
from django.contrib import admin

from .views import (
    UserRegistrationAPIView,
    LoginUser
    )
from rest_framework_simplejwt import views as jwt_views
app_name="users-api"

urlpatterns = [
    url(r'^login/$', LoginUser.as_view(), name='login'),
    url(r'^register/$', UserRegistrationAPIView.as_view(), name='register'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/verify/', jwt_views.TokenVerifyView.as_view()),
]
