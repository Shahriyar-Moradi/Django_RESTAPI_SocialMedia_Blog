from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework import routers
from .views import LikeViewSet,PostViewSet,CommentViewSet,UserViewSet


router = routers.DefaultRouter()
router.register(r'post', PostViewSet)
router.register(r'comment', CommentViewSet)


urlpatterns = [
    path('', include(router.urls)),

    path('user/', UserViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='user_list'),

    path('like/', LikeViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='comment_list')
]
