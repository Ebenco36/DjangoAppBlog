from django.urls import path, include
from django.contrib import admin

from .views import (
        CommentCreateAPIView,
        CommentDetailAPIView,
        CommentListAPIView,
    )
app_name = 'comments-api'
urlpatterns = [
    path('', CommentListAPIView.as_view(), name='list'),
    path('create/', CommentCreateAPIView.as_view(), name='create'),
    path('<pk>/', CommentDetailAPIView.as_view(), name='thread'),
    #url(r'^(?P<id>\d+)/delete/$', comment_delete, name='delete'),
]
