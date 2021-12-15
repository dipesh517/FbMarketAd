from django.urls import path
from . import views

urlpatterns = [
  path('', views.CampaignList.as_view()),
  path('<string:pk>/', views.CampaignDetail.as_view()),
  path('accountSecrets',views.AccountSecretsView.as_view())
]

