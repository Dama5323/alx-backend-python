import django_filters
from django.utils import timezone
from datetime import timedelta
from .models import Message
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageFilter(django_filters.FilterSet):
    conversation = django_filters.UUIDFilter(field_name='conversation__id')
    participant = django_filters.UUIDFilter(field_name='conversation__participants__id')
    sender = django_filters.ModelChoiceFilter(queryset=User.objects.all())
    sent_after = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
    sent_before = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')

    # Time range filters
    start_date = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')

    # Last N days filter
    last_days = django_filters.NumberFilter(method='filter_last_days')

    class Meta:
        model = Message
        fields = ['sender', 'conversation', 'sent_after', 'sent_before', 'start_date', 'end_date', 'last_days']

    def filter_last_days(self, queryset, name, value):
        if value:
            cutoff_date = timezone.now() - timedelta(days=int(value))
            return queryset.filter(sent_at__gte=cutoff_date)
        return queryset
