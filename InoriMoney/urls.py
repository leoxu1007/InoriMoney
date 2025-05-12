"""
URL configuration for InoriMoney project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
import books.views as books_views
import imports.views as imports_views
import converts.views as converts_views
import news.views as news_views
urlpatterns = [
    path("", books_views.index),
    path("upload", imports_views.upload),
    path("clear-cache", imports_views.clear_cache),
    path("convert", converts_views.index),
    path('admin', admin.site.urls),
    path('new-pay', news_views.new_pay),
    path('new-receive', news_views.new_receive),
    path('new-transfer', news_views.new_transfer),
    path('new-loan', news_views.new_loan),
]
