from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import ConfCodeSerializer
from .views import UserViewSet, mail_code

router = DefaultRouter()

router.register("users", UserViewSet)

urlpatterns = [
    path("v1/auth/signup/", mail_code),
    path(
        "v1/auth/token/",
        TokenObtainPairView.as_view(serializer_class=ConfCodeSerializer),
        name="token_obtain_pair",
    ),
    path("v1/", include(router.urls)),
]
