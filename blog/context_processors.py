#<!-- filepath: d:\Desktop\fotoblog\fotoblog\blog\templates\blog\context_processors.py -->

from .models import Notification

def unread_notifications(request):
    if request.user.is_authenticated:
        return {
            'has_unread_notifications': Notification.objects.filter(is_read=False).exists()
        }
    return {}