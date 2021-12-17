from django.urls import path
from . import views

urlpatterns = [
  path('', views.AdsetList.as_view()),
  path('<int:pk>/', views.AdsetDetail.as_view()),
]