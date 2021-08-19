from django.conf.urls import url  # noqa
from django.urls import path, include
from django.contrib import admin
import django_js_reverse.views
from django.views.generic import TemplateView


urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("jsreverse/", django_js_reverse.views.urls_js, name="js_reverse"),
    path('', include('battle.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/', include('battle.urls_api')),
    path("react/battle/detail/<int:pk>/", TemplateView.as_view(template_name="react/react_template.html"), name="react_template"),
]
