
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('campaign/', include('AdCampaign.urls')),
    path('admin/', admin.site.urls),
]
