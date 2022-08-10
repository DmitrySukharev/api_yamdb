from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import User
from .utils import generate_conf_code, confirmation_mail

# User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def mail_code(request):
    email = request.data.get('email')
    #user = get_object_or_404(User, email=email)
    user = User.objects.create(
        username=request.data.get('username'),
        email=email,
    )
    code = generate_conf_code()

    confirmation_mail(email, code)
    user.confirmation_code = code
    user.save()

    return Response({'email': email})

