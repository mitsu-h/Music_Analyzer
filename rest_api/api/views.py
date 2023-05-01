from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework import generics, status

from .serializers import UserSerializer
from .models import CustomUser
from .utils import youtube

from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(["GET"])
def hello(request):
    return Response({"message": "Hello from Django!"})


@api_view(["GET"])
def get_video_info(request):
    url = request.GET.get("url", None)
    if not url:
        return Response(
            {"error": "URL parameter is required."}, status=status.HTTP_400_BAD_REQUEST
        )

    video_info = youtube.get_video_info(url)
    if not video_info:
        return Response(
            {"error": "Failed to get video information. Check the URL."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    return Response(video_info)
