from django.urls import path
from api.battle import views

urlpatterns = [
    path('battles/', views.BattletList.as_view(), name="battle-list"),
    path("battle/<int:pk>/", views.BattleDetail.as_view(), name="battle-detail"),
]
