# -*- coding: utf-8 -*-
# @Time    : 2018/10/16 20:59
# @Author  : ZengQingheng
# @Email   : 1107753149@qq.com
# @File    : urls.py
# @Software: PyCharm
"""qingheng_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from blog.views import index,archive,article,tag_archive


urlpatterns = [
    path('',index,name='index'),
    path("archive/",archive,name="archive"),
    path("article/",article,name="article"),
    path("tag_archive/",tag_archive,name="tag_archive"),
]