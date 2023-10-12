from account.models import User

from django.contrib.auth import login

from knox.views import LoginView as KnoxLoginView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.serializers import AuthTokenSerializer

from .serializers import UserModelSerializer


class UserModelViewSet(ModelViewSet):
    """
    A viewset for viewing and editing User instances.
    """
    serializer_class = UserModelSerializer
    queryset = User.objects.all()


class RegisterView(APIView):
    """
    API endpoint that allows users to register.
    """
    permission_classes = [AllowAny]
    
    def post(self, request, format=None):
        serializer = UserModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(**serializer.validated_data)
        serializer = UserModelSerializer(user)
        return Response({
            "data": serializer.data,
        })


class LoginView(KnoxLoginView):
    """
    View for user login. Accepts POST requests with username and password in request data.
    Returns a token if authentication is successful.
    """
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)
    

