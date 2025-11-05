from rest_framework import serializers
from .models import Movie, Comment, Like
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class MovieSerializer(serializers.ModelSerializer):
    comments_count = serializers.IntegerField(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'description', 'release_date', 'duration',
            'poster', 'likes_count', 'comments_count'
        ]
        read_only_fields = ['likes_count', 'comments_count']


class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id', 'movie', 'author', 'author_username', 'text',
            'parent', 'created_at', 'updated_at', 'likes_count', 'replies'
        ]
        read_only_fields = ['author', 'created_at', 'updated_at', 'likes_count', 'replies']

    def get_replies(self, obj):
        replies = Comment.objects.filter(parent=obj)
        return CommentSerializer(replies, many=True).data


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'movie', 'user', 'value', 'created_at']
        read_only_fields = ['user', 'created_at']