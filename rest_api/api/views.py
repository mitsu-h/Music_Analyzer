import base64
import json
import os

import boto3
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework import generics, status

from .serializers import UserSerializer, AnalysisResultsSerializer
from .models import CustomUser
from .utils.youtube import _get_video_info, download_youtube_audio_info
from .utils.separate import separate_and_upload_to_s3
from .utils.dynamodb import get_dynamodb_client, put_analyze_info

from django.contrib.auth import get_user_model

User = get_user_model()

# S3クライアントの作成
endpoint_url = os.getenv("S3_ENDPOINT")
s3_client = boto3.client("s3", endpoint_url=endpoint_url)
dynamodb_client = get_dynamodb_client()


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

    video_info = _get_video_info(url)
    if not video_info:
        return Response(
            {"error": "Failed to get video information. Check the URL."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    return Response(video_info)


@api_view(["GET"])
def get_analysis_by_user_id(request, user_id):
    response = dynamodb_client.query(
        TableName="AnalysisResults",
        KeyConditionExpression="user_id = :user_id",
        ExpressionAttributeValues={":user_id": {"S": user_id}},
    )
    serializer = AnalysisResultsSerializer(response["Items"], many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_audio_file(request):
    audio_file_path = request.GET.get("audio_file_path")
    print(audio_file_path)

    if audio_file_path:
        response = s3_client.get_object(
            Bucket="music", Key=audio_file_path.replace("s3://music/", "")
        )
        audio_file_data = response["Body"].read()
        audio_files_data_base64 = base64.b64encode(audio_file_data).decode("utf-8")

        return JsonResponse({"audio_file_data": audio_files_data_base64})
    else:
        return Response(
            {"error": "audio_file_path is required"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["GET"])
def download_and_separate_audio(request):
    user_id = request.GET.get("user_id")
    url = request.GET.get("url")
    title = request.GET.get("title")
    artist = request.GET.get("artist")

    # get youtube audio
    (
        original_audio_file,
        description,
        duration,
        original_audio_path,
    ) = download_youtube_audio_info(url, s3_client, output_s3_bucket="music")
    separated_audio_files = separate_and_upload_to_s3(original_audio_file, s3_client)
    put_analyze_info(
        user_id,
        url,
        title,
        artist,
        description,
        original_audio_path,
        separated_audio_files,
        duration,
        dynamodb_client,
    )
    return HttpResponse("success separate and put dynamo db!")
