from rest_framework import serializers

from blog.models import Post, Comment, PostLiked
from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema_field


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class PostLikedSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = PostLiked
        fields = ['user', 'username', 'is_liked', 'post']


class PostSerializer(serializers.ModelSerializer):
    post_author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)
    author = serializers.CharField(source='post_author.username', read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ['text', 'author', 'post_author', 'likes_count', 'comments']

    def create(self, validated_data):
        post_author = validated_data.pop('post_author')
        post = Post.objects.create(post_author=post_author, **validated_data)
        return post

    @extend_schema_field(str)
    def get_likes_count(self, obj):
        like_count = PostLiked.objects.filter(post=obj).count()
        return like_count

    @extend_schema_field(str)
    def get_comments(self, obj):
        # comments=Comment.objects.filter(post=obj)
        comments = Comment.objects.filter(post=obj).all()
        serializer = CommentSerializer(comments, many=True)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), write_only=True)
    reply = serializers.CharField(read_only=True)

    class Meta:
        model = Comment
        fields = ['user', 'username', 'text', 'post', 'reply']

    def get_replies(self, comment):
        serializer = CommentSerializer(comment.replies.all(), many=True)
        return serializer.data
