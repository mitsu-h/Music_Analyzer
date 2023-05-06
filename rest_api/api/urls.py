from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from .views import RegisterUserView

urlpatterns = [
    path("account/register/", RegisterUserView.as_view(), name="register_user"),
    path("account/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("account/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("rest-auth/", include("dj_rest_auth.urls")),
    path("rest-auth/registration/", include("dj_rest_auth.registration.urls")),
    path("music/video_info/", views.get_video_info, name="video_info"),
    path(
        "analysis_results/<str:user_id>",
        views.get_analysis_by_user_id,
        name="get_analysis_by_user_id",
    ),
]
