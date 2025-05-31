# Example view usage
from rest_framework import generics
from .models import Conversation
from .serializers import ConversationSerializer

class ConversationDetailView(generics.RetrieveAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
