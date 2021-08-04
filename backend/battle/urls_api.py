from django.urls import path
from battle import endpoints

urlpatterns = [
    path('battles/', endpoints.BattletList.as_view(), name="battle-list"),
    path("battle/<int:pk>/", endpoints.BattleDetail.as_view(), name="battle-detail"),
]
