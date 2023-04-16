from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework import generics

from .serializers import UserSerializer
from .models import CustomUser

from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(["GET"])
def hello(request):
    return Response({"message": "Hello from Django!"})
