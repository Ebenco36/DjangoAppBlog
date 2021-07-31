from django.conf import settings
from django.db.models.expressions import Exists, OuterRef
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny  # <-- Here
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK, HTTP_201_CREATED
)
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.views import TokenObtainPairView


class UserRegistrationAPIView(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            data = serializer.data
            headers = self.get_success_headers(serializer.data)
            return Response({'status':'success', 'data':'user created successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'status':'failed', 'data':serializer.errors['non_field_errors'][0] if ('non_field_errors' in serializer.errors) else serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



class LoginUser(TokenObtainPairView):
    serializer_class = LoginUserSerializer


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    if email is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(email=email, password=password)
    print(user)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)





















