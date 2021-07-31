"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url('$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url('$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url('blog/', include(blog_urls))
"""
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token

from accounts.views import (login_view, register_view, logout_view)

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('comments/', include("comments.urls", namespace='comments')),
    
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', include("posts.urls", namespace='posts')),
    path('api/auth/token/', obtain_jwt_token),
    path('api/users/', include("accounts.api.urls", namespace='users-api')),
    path('api/comments/', include("comments.api.urls", namespace='comments-api')),
    path('api/posts/', include("posts.api.urls", namespace='posts-api')),
    #url('posts/$', "<appname>.views.<function_name>"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)