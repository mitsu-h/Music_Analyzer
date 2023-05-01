# api/tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


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
