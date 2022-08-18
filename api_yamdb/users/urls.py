from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import ConfCodeSerializer, RegSerializer
from .views import UserViewSet, mail_code, MailCodeView

router = DefaultRouter()

router.register("users", UserViewSet)

urlpatterns = [
    path("signup/", mail_code),
   # path(
   #     "signup/", 
   #     MailCodeView.as_view(),
   #     name="mail_code"
   # ),
    path(
        "token/",
        TokenObtainPairView.as_view(serializer_class=ConfCodeSerializer),
        name="token_obtain_pair",
    ),
    path("", include(router.urls)),
]
