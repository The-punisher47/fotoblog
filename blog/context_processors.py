#<!-- filepath: d:\Desktop\fotoblog\fotoblog\blog\templates\blog\context_processors.py -->

from .models import Notification

def unread_notifications(request):
    if request.user.is_authenticated:
        return {
            'has_unread_notifications': Notification.objects.filter(is_read=False).exists()
        }
    return {}

def notifications_processor(request):
    if request.user.is_authenticated:
        return {
            'notifications': Notification.objects.filter(is_read=False).order_by('-created_at')
        }
    return {}  # Ne retourne rien si l'utilisateur n'est pas connecté
