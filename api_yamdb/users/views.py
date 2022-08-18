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
from .serializers import UserSerializer, RegSerializer
from .utils import confirmation_mail, email_check, generate_conf_code
from rest_framework.views import APIView

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

#####

def email_unique(new_email):
    current_emails = []
    users = User.objects.all()
    for user in users:
        current_emails.append(user.email)
    
    if new_email in current_emails:
        return False
    
    return True


class MailCodeView(APIView):
    serializer_class = RegSerializer
    
    def mail(self, serializer):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=False)
        
        code = generate_conf_code()
        confirmation_mail(email, code)
        
        serializer.save()
        return Response(serializer.data)


def without_data(email, username):
    fields = {"email": email, "username": username}
    missing = []
    for field in fields:
        if fields[field] is None:
            missing.append(field)

    message = f'missing fields: {missing}'

    if missing:
        return Response({message}, status=status.HTTP_400_BAD_REQUEST)


#####

@api_view(["POST"])
@permission_classes([AllowAny])
def mail_code(request):
    
   # if "username" not in request.data and "email" not in request.data:
    #    raise ValidationError
        
    email = request.data.get("email")
    username = request.data.get("username")

    without_data(email, username)
    
    if email is None or username is None:
        if email is None:   
            return Response({"email": "expected"}, status=status.HTTP_400_BAD_REQUEST)
        elif username is None:
            return Response({"username": "expected"}, status=status.HTTP_400_BAD_REQUEST)

    if not email_unique(email):
        message = f"User with email {email} already exists"
        return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

    if username == 'me' or username is None:
        message = "restricted username"
        return Response({"username": message}, status=status.HTTP_400_BAD_REQUEST)

   # if not request.data:
   #     message = "no data"
   #     return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

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
            return Response({"message": message})

    return Response({"email": email, "username": username}, status=status.HTTP_200_OK)
