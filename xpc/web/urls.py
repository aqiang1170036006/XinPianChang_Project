"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from web.views import post, composer

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', post.index),
    url(r'^list/(?P<page>\d+)/$', post.index),
    url(r'user/oneuser/userid-(?P<cid>\d+)$', composer.oneuser),
    url(r'a(?P<pid>\d+)$', post.detail),
    url(r'u(?P<cid>\d+)$', composer.homepage),
    url(r'comments$', post.comments),
    url(r'index.php', post.index_php),
    url(r'article/filmplay/ts-viewed', post.ts_view),
]
