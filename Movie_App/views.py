from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from .models import Movie, Comment, Like
from .serializers import MovieSerializer, CommentSerializer, LikeSerializer

User = get_user_model()


class MovieListCreateView(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAdminUser]

class MovieDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAdminUser]


class MovieDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAdminUser]


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.filter(parent__isnull=True)
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class LikeToggleView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        movie_id = request.data.get('movie')
        value = int(request.data.get('value', 1))

        if value not in [1, -1]:
            return Response("Value: 1 or -1", status=400)

        try:
            movie = Movie.objects.get(id=movie_id)
        except:
            return Response("Movie not found", status=404)

        like, created = Like.objects.update_or_create(
            movie=movie, user=request.user, defaults={'value': value}
        )

        if not created and like.value == value:
            like.delete()
            return Response("Removed", status=200)

        return Response(LikeSerializer(like).data, status=201)


class MovieCommentsView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(movie_id=self.kwargs['movie_id'], parent__isnull=True)


class MovieLikesView(generics.ListAPIView):
    serializer_class = LikeSerializer

    def get_queryset(self):
        return Like.objects.filter(movie_id=self.kwargs['movie_id'])


from .serializers import UserRegisterSerializer  

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegisterSerializer  

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response("Registered!", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        return self.request.user