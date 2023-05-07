import base64
import json
import os

import boto3
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework import generics, status

from .serializers import UserSerializer, AnalysisResultsSerializer
from .models import CustomUser
from .utils import youtube
from .utils.dynamodb import get_dynamodb_client

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


@api_view(["GET"])
def get_analysis_by_user_id(request, user_id):
    dynamodb_client = get_dynamodb_client()
    response = dynamodb_client.query(
        TableName="AnalysisResults",
        KeyConditionExpression="user_id = :user_id",
        ExpressionAttributeValues={":user_id": {"S": user_id}},
    )
    serializer = AnalysisResultsSerializer(response["Items"], many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_audio_file(request):
    audio_file_path = json.loads(request.GET.get("separated_audio_files"))
    print(audio_file_path)

    if audio_file_path:
        endpoint_url = os.getenv("S3_ENDPOINT")
        # S3クライアントの作成
        s3_client = boto3.client("s3", endpoint_url=endpoint_url)

        audio_files_data = {}
        for key, audio_file_path in audio_file_path.items():
            response = s3_client.get_object(
                Bucket="music", Key=audio_file_path.replace("s3://music/", "")
            )
            audio_file_data = response["Body"].read()
            audio_files_data[key] = base64.b64encode(audio_file_data).decode("utf-8")

        return JsonResponse(audio_files_data)
    else:
        return Response(
            {"error": "audio_file_path is required"}, status=status.HTTP_400_BAD_REQUEST
        )
