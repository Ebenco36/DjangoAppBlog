from django.urls import path, include
from django.contrib import admin

from .views import (
	post_list,
	post_create,
	post_detail,
	post_update,
	post_delete,
	)

app_name = 'posts'

urlpatterns = [
	path('', post_list, name='list'),
    path('create/', post_create),
    path('<slug>/', post_detail, name='detail'),
    path('<slug>/edit/', post_update, name='update'),
    path('<slug>/delete', post_delete),
    #url(r'^posts/$', "<appname>.views.<function_name>"),
]
