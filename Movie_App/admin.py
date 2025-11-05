from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Movie, Comment, Like

User = get_user_model()

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'duration', 'likes_count', 'comments_count')
    search_fields = ('title',)
    readonly_fields = ('likes_count', 'comments_count')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('movie', 'author', 'text', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('text',)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'value', 'created_at')
    list_filter = ('value', 'created_at')