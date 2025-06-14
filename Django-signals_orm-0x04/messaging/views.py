from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message, MessageHistory
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from django.db.models import Prefetch


@login_required
def message_history(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    
    # Verify the user has permission to view this message
    if request.user not in [message.sender, message.receiver]:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden()
    
    history = message.history.all().order_by('-edited_at')
    
    return render(request, 'messaging/message_history.html', {
        'message': message,
        'history': history
    })


@login_required
@require_POST
def delete_user(request):
    """View to delete user account and all related data"""
    user = request.user
    logout(request)  # Logout before deletion
    user.delete()  # This will trigger the post_delete signal
    
    messages.success(request, 'Your account has been permanently deleted.')
    return redirect('home')  # Redirect to home page

def message_thread(request, message_id):
    # Get the root message with optimized queries
    message = get_object_or_404(
        Message.objects
        .select_related('sender', 'receiver')
        .prefetch_related(
            Prefetch('replies',
                queryset=Message.objects
                    .select_related('sender')
                    .order_by('timestamp')
            )
        ),
        pk=message_id
    )

def get_replies(message, depth=0):
        replies = []
        for reply in message.replies.all():
            replies.append({
                'message': reply,
                'depth': depth + 1,
                'replies': get_replies(reply, depth + 1)
            })
        return replies
    
        thread = {
        'message': message,
        'replies': get_replies(message)
    }
    
        return render(request, 'messaging/message_thread.html', {
        'thread': thread
    })