"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from home import views
urlpatterns = [    
    path('', views.PostList.as_view(), name='home'),
    path('verify/<auth_token>',views.verify, name="verify"),
    path('token/',views.token_send, name='token_send'),
    path('register/',views.register, name="register"),
    path('login/',views.login,name="login"),
    path('success/',views.success,name="success"),
    path('error',views.error_page,name="error"),
    path('reset_verify/<auth_token>',views.reset_verify, name="reset_verify"),
    path('forget_password',views.forget_password,name="forget_password"),
    path('reset_password',views.reset_password,name="reset_password"),
    path('createblog/',views.createblog, name="createblog"),
    path('search/',views.search,name="search"),
    path('<slug:slug>/',views.post_detail,name='post_detail'),
    
]
