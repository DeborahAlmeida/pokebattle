from django.conf.urls import url  # noqa
from django.urls import path, include
from django.contrib import admin
import django_js_reverse.views


urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("jsreverse/", django_js_reverse.views.urls_js, name="js_reverse"),
    path('', include('battle.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
