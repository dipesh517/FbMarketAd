
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('campaign/', include('AdCampaign.urls')),
    path('adset/', include('adset.urls')),
    path('ads/', include('ads.urls')),
    path('admin/', admin.site.urls),
]
