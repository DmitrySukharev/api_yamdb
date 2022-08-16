from django.core.validators import validate_email
from django.http import Http404
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from rest_framework import status
from .models import User
from .permissions import IsAdmin
from .serializers import UserSerializer
from .utils import confirmation_mail, email_check, generate_conf_code


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAdmin,]
    serializer_class = UserSerializer
    lookup_field = "username"
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "username",
    ]

    @action(
        methods=["patch", "get"],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path="me",
        url_name="me",
    )
    def me(self, request, *args, **kwargs):
        instance = self.request.user
        serializer = self.get_serializer(instance)
        if self.request.method == "PATCH":
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid()
            serializer.save()
        return Response(serializer.data)


@api_view(["POST"])
@permission_classes([AllowAny])
def mail_code(request):
    
   # if "username" not in request.data and "email" not in request.data:
    #    raise ValidationError
    
    email = request.data.get("email")
    username = request.data.get("username")

    if not request.data:
        message = "no data"
        return Response({"email": message}, status=status.HTTP_400_BAD_REQUEST)

    if not email:
        message = "Have not any email? In this case try to guess your code"

    else:
        if email_check(email):
            try:
                user = get_object_or_404(User, email=email)
            except Http404:
                user = User.objects.create(
                    username=username,
                    email=email,
                )

            code = generate_conf_code()

            confirmation_mail(email, code)
            user.confirmation_code = code
            message = "confirmation code has been sent on your email"
            user.save()
        else:
            message = "You should provide valid email"

    return Response({"email": message})
