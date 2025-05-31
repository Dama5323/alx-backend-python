from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chats.urls')),           # ✅ Your app's API
    path('api-auth/', include('rest_framework.urls')),  # ✅ Enables DRF login/logout
]
