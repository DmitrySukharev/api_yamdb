from .views import mail_code
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)


urlpatterns = [
    path('v1/auth/signup/', mail_code),
    path('v1/auth/token/',  TokenObtainPairView.as_view(),
        name='token_obtain_pair'),
]
                            
