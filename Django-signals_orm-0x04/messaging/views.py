from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from django.db.models import Prefetch
from .models import Message, MessageHistory

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
    return redirect('home')

@login_required
def message_thread(request, message_id):
    # Get the root message with optimized queries
    message = get_object_or_404(
        Message.objects
        .select_related('sender', 'receiver')
        .prefetch_related(
            Prefetch('replies',
                queryset=Message.objects
                    .select_related('sender')
                    .filter(sender=request.user)  # Filter by current user
                    .order_by('timestamp')
            )
        ),
        pk=message_id,
        sender=request.user  # Ensure user owns the message
    )
    
    # Get all replies in the thread (recursive)
    def get_all_replies(message):
        return Message.objects.filter(
            parent_message=message
        ).select_related('sender').prefetch_related(
            Prefetch('replies', queryset=Message.objects.select_related('sender'))
        )
    
    replies = get_all_replies(message)
    
    context = {
        'message': message,
        'replies': replies
    }
    
    return render(request, 'messaging/message_thread.html', context)