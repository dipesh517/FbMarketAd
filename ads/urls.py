from django.urls import path
from . import views

urlpatterns = [
  path('', views.AdsList.as_view()),
  path('adCreative/', views.AdCreativeList.as_view()),
  path('adCreative/<int:pk>', views.AdCreativeDetail.as_view()),
]