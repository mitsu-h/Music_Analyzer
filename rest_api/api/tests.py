# api/tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .serializers import AnalysisResultsSerializer
from uuid import UUID
import uuid


class VideoInfoAPITests(APITestCase):
    def test_get_video_info_success(self):
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        response = self.client.get(reverse("video_info"), {"url": url})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("title", response.data)
        self.assertIn("channel", response.data)

    def test_get_video_info_missing_url(self):
        response = self.client.get(reverse("video_info"))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_get_video_info_invalid_url(self):
        url = "https://www.example.com/invalid_url"
        response = self.client.get(reverse("video_info"), {"url": url})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)


class GetAnalysisByUserIdTestCase(APITestCase):
    def setUp(self):
        self.user_id = uuid.uuid4()

        self.analysis_result_1 = AnalysisResults.objects.create(
            user_id=self.user_id,
            analysis_id=uuid.uuid4(),
            youtube_video_id="video_id_1",
            youtube_title="Title 1",
            youtube_channel="Channel 1",
            youtube_description="Description 1",
            source_type="youtube",
            uploaded_audio_file=None,
            downloaded_audio_file="s3://bucket/audio_1.mp3",
            separated_audio_files='{"vocals": "s3://bucket/vocals_1.mp3", "accompaniment": "s3://bucket/accompaniment_1.mp3"}',
            last_played_position=0,
            loop_intervals='[{"start": 10, "end": 20}]',
            playback_speed=1.0,
            instruments_volume='{"vocals": 1.0, "accompaniment": 1.0}',
            created_at="2023-01-01T00:00:00Z",
            updated_at="2023-01-01T00:00:00Z",
            comment="Test comment 1",
        )

    self.analysis_result_2 = AnalysisResults.objects.create(
        user_id=self.user_id,
        analysis_id=uuid.uuid4(),
        youtube_video_id=None,
        youtube_title=None,
        youtube_channel=None,
        youtube_description=None,
        source_type="upload",
        uploaded_audio_file="s3://bucket/uploaded_audio_2.mp3",
        downloaded_audio_file=None,
        separated_audio_files='{"vocals": "s3://bucket/vocals_2.mp3", "accompaniment": "s3://bucket/accompaniment_2.mp3"}',
        last_played_position=0,
        loop_intervals='[{"start": 30, "end": 40}]',
        playback_speed=1.0,
        instruments_volume='{"vocals": 1.0, "accompaniment": 1.0}',
        created_at="2023-01-01T00:00:00Z",
        updated_at="2023-01-01T00:00:00Z",
        comment="Test comment 2",
    )

    self.other_user_analysis_result = AnalysisResults.objects.create(
        user_id=uuid.uuid4(),
        analysis_id=uuid.uuid4(),
        youtube_video_id="video_id_3",
        youtube_title="Title 3",
        youtube_channel="Channel 3",
        youtube_description="Description 3",
        source_type="youtube",
        uploaded_audio_file=None,
        downloaded_audio_file="s3://bucket/audio_3.mp3",
        separated_audio_files='{"vocals": "s3://bucket/vocals_3.mp3", "accompaniment": "s3://bucket/accompaniment_3.mp3"}',
        last_played_position=0,
        loop_intervals='[{"start": 50, "end": 60}]',
        playback_speed=1.0,
        instruments_volume='{"vocals": 1.0, "accompaniment": 1.0}',
        created_at="2023-01-01T00:00:00Z",
        updated_at="2023-01-01T00:00:00Z",
        comment="Test comment 2",
    )

    def test_get_analysis_by_user_id(self):
        url = reverse("analysis-results-list")
        response = self.client.get(url, {"user_id": self.user_id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertEqual(len(response_data), 2)

        expected_data = AnalysisResultsSerializer(
            [self.analysis_result_1, self.analysis_result_2], many=True
        ).data
        self.assertEqual(response_data, expected_data)
