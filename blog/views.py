from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from .models import Post, PostLiked, Comment, User
from .serializers import PostSerializer, CommentSerializer, PostLikedSerializer, UserSerializer

from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers

from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework import viewsets


class PostViewSet(viewsets.ViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @extend_schema(responses=PostSerializer)
    def list(self, request):
        serializer = PostSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False, url_path=r"(?P<author_id>\w+)/all")
    def list_post_by_author(self, request, author_id):
        serializer = PostSerializer(self.queryset.filter(post_author_id=author_id), many=True)
        print('get by author')
        return Response(serializer.data)

    def create(self, request):
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CommentViewSet(viewsets.ViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    @extend_schema(responses=PostSerializer)
    def list(self, request):
        serializer = CommentSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False, url_path=r"(?P<post_id>\w+)/all")
    def list_comment_by_post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.validated_data['username']
        print("username", user)

        # Check if the user with specific name is already created
        new_user = User.objects.filter(username=user)
        if new_user.exists():
            raise serializers.ValidationError(f"User with name {user} is already created.")
        else:
            serializer.save()
            serializer = UserSerializer()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = PostLiked.objects.all()
    serializer_class = PostLikedSerializer

    def perform_create(self, serializer):
        like = serializer.validated_data['is_liked']
        user = serializer.validated_data['user']
        post = serializer.validated_data['post']
        print("user", user)
        print('is_liked : ', like)
        new_liked = PostLiked.objects.filter(
            is_liked=True, post=post, user=user)
        if new_liked.exists():
            raise serializers.ValidationError(f"You have liked is post already.")
        else:
            serializer.save()
            serializer = PostLikedSerializer()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentReplyView(viewsets.ViewSet):
    queryset = Post.objects.all()
    serializer_class = CommentSerializer
