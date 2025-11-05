# Movie_App/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from . import views

schema_view = get_schema_view(
    openapi.Info(title="Test API", default_version='v1'),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('movies/', views.MovieListCreateView.as_view(), name='movie-list'),
    path('movies/<int:pk>/', views.MovieDetailView.as_view(), name='movie-detail'),  # ← ИСПРАВИЛ

    path('comments/', views.CommentListCreateView.as_view(), name='comment-list'),
    path('comments/<int:pk>/', views.CommentDetailView.as_view(), name='comment-detail'),

    path('like/', views.LikeToggleView.as_view(), name='like-toggle'),

    path('movies/<int:movie_id>/comments/', views.MovieCommentsView.as_view(), name='movie-comments'),
    path('movies/<int:movie_id>/likes/', views.MovieLikesView.as_view(), name='movie-likes'),

    path('auth/jwt/create/', TokenObtainPairView.as_view(), name='jwt-create'),  # ← ОДИН РАЗ!
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/me/', views.MeView.as_view(), name='me'),

    path('swagger/', schema_view.with_ui('swagger'), name='swagger'),
    path('redoc/', schema_view.with_ui('redoc'), name='redoc'),
]