from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView  
)

def home(request):
    return HttpResponse("🎉 Welcome to the Messaging App API!")

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    
    # API Routes
    path('api/', include([
        path('', include('chats.urls')),  
        
        # JWT Authentication
        path('auth/', include([
            path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
            path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
            path('verify/', TokenVerifyView.as_view(), name='token_verify'),  # New
        ])),
    ])),
    
    # DRF Browsable API Auth
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]