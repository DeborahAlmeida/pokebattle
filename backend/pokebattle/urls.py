from django.conf.urls import url  # noqa
from django.urls import path, include
from django.contrib import admin
from django.views.generic import TemplateView

import django_js_reverse.views

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("jsreverse/", django_js_reverse.views.urls_js, name="js_reverse"),
    path('', include('battle.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/', include('battle.urls_api')),
    path(
        "v2/battle/detail/<int:pk>/",
        TemplateView.as_view(template_name="spa/spa_template.html"),
        name="spa_template"),
]
