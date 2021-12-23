from django.urls import path
from . import views

urlpatterns = [
  path('', views.AdsList.as_view()),
  path('adCreative/', views.AdCreative.as_view())
]