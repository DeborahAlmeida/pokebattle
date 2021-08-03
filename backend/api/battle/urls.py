from django.urls import path
from api.battle import views

urlpatterns = [
    path('battles/', views.BattletList.as_view()),
]
