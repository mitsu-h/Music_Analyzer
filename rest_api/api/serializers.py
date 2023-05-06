from rest_framework import serializers
from dj_rest_auth.registration.serializers import (
    RegisterSerializer as DefaultRegisterSerializer,
)
from dj_rest_auth.serializers import UserDetailsSerializer
from allauth.utils import email_address_exists, get_username_max_length

from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "password")

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"], password=validated_data["password"]
        )
        return user


class DynamoDBField(serializers.Field):
    def to_representation(self, value):
        return list(value.values())[0]


class AnalysisResultsSerializer(serializers.Serializer):
    user_id = DynamoDBField()
    analysis_id = DynamoDBField()
    youtube_video_url = DynamoDBField(required=False, allow_null=True)
    title = DynamoDBField()
    artist = DynamoDBField()
    youtube_description = DynamoDBField(required=False, allow_null=True)
    source_type = (
        DynamoDBField()
    )  # choices=[("youtube", "youtube"), ("upload", "upload")]
    audio_file = DynamoDBField()
    separated_audio_files = DynamoDBField()
    last_played_position = DynamoDBField()
    loop_intervals = DynamoDBField()
    playback_speed = DynamoDBField()
    instruments_volume = DynamoDBField()
    created_at = DynamoDBField()
    updated_at = DynamoDBField()
    comment = DynamoDBField()  # allow_blank=True

    def validate(self, data):
        if data["source_type"] == "youtube":
            if "youtube_video_url" not in data or "youtube_description" not in data:
                raise serializers.ValidationError(
                    "youtube_video_url and youtube_description are required for source_type 'youtube'"
                )
        elif data["source_type"] == "upload":
            if "youtube_video_url" in data or "youtube_description" in data:
                raise serializers.ValidationError(
                    "youtube_video_url and youtube_description should not be provided for source_type 'upload'"
                )
        return data
