from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('results-api/', include('results.api.urls')),
    path('comments-api/', include('comments.api.urls')),
]
