from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path(
        "battle/detail/<int:pk>/",
        TemplateView.as_view(template_name="spa/spa_template.html"),
        name="battle_detail_v2"),
]
