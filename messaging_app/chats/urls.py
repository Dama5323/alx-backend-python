from django.urls import path, include
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from .views import ConversationViewSet, MessageViewSet

# ✅ Step 1: Create base router and register conversations
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# ✅ Step 2: Create nested router for messages under conversations
convo_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
convo_router.register(r'messages', MessageViewSet, basename='conversation-messages')

# ✅ Step 3: Combine all routes
urlpatterns = [
    path('', include(router.urls)),
    path('', include(convo_router.urls)),
]
