from django.contrib import admin
from django.urls import path, re_path
from django.shortcuts import render

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda r: render(r, 'base.html'), name='home'),
    path('about/', lambda r: render(r, 'base.html'), name='about'),

    re_path(r'^(?P<slug>[\w/-]+)/$', lambda r, slug: render(r, 'base.html')),
]
