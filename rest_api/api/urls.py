from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from .views import RegisterUserView

urlpatterns = [
    path("check_token/", views.check_token, name="check_token"),
    path("account/register/", RegisterUserView.as_view(), name="register_user"),
    path("account/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("account/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("rest-auth/", include("dj_rest_auth.urls")),
    path("rest-auth/registration/", include("dj_rest_auth.registration.urls")),
    path("music/video_info/", views.get_video_info, name="video_info"),
    path(
        "analysis_results/",
        views.get_analysis_by_user_id,
        name="get_analysis_by_user_id",
    ),
    path("get_audio_file/", views.get_audio_file, name="get_audio_file"),
    path(
        "download_and_separate_audio/",
        views.download_and_separate_audio,
        name="download_and_separate_audio",
    ),
    path('save_to_dynamodb/', views.save_to_dynamodb, name='save_to_dynamodb'),
]
