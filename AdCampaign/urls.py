from django.urls import path
from . import views

urlpatterns = [
  path('', views.CampaignList.as_view()),
  path('<int:pk>/', views.CampaignDetail.as_view()),
]

