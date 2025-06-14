from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message, MessageHistory

@login_required
def message_history(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    history = message.history.all().order_by('-edited_at')
    
    # Verify the user has permission to view this message
    if request.user not in [message.sender, message.receiver]:
        return HttpResponseForbidden()
    
    return render(request, 'messaging/message_history.html', {
        'message': message,
        'history': history
    })