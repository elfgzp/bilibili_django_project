"""bilibili_django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from bilibili_danmu import views

urlpatterns = [
    url(r'^tools', views.app),
    url(r'^', admin.site.urls),
    url(r'^get_bilibili_cookie', views.get_bilibili_cookie),
    url(r'^get_bilibili_captcha', views.get_bilibili_captcha),
    url(r'^apilivebilibilicom/(.+)', views.api_live_bilibili_com),
    url(r'^livebilibilicom/(.+)', views.live_bilibili_com),
    url(r'^apibilibilicom/(.+)', views.api_bilibili_com),

]
