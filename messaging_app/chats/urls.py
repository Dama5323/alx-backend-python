# chats/urls.py
from django.urls import path, include
from rest_framework import routers  # ✅ use "routers", not just "DefaultRouter"
from .views import ConversationViewSet, MessageViewSet

router = routers.DefaultRouter()  # ✅ Must use this line exactly

router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
]
