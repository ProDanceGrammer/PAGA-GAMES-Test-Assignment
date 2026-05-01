"""
Utility functions for the integrations app
"""
from datetime import datetime
from django.utils import timezone


def format_date_for_display(date_obj):
    """Format datetime for user-friendly display"""
    if not date_obj:
        return 'N/A'

    now = timezone.now()
    diff = now - date_obj

    if diff.days == 0:
        return 'Today'
    elif diff.days == 1:
        return 'Yesterday'
    elif diff.days < 7:
        return f'{diff.days} days ago'
    else:
        return date_obj.strftime('%B %d, %Y')


def truncate_text(text, max_length=100):
    """Truncate text to specified length with ellipsis"""
    if not text or len(text) <= max_length:
        return text
    return text[:max_length].rsplit(' ', 1)[0] + '...'
