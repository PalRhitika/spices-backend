from celery import shared_task
from users.models import User
from .models import Notification

@shared_task
def send_connection_notification(from_user_id, to_user_id, status):
    print('yeta aayo bhai')
    from_user = User.objects.get(id=from_user_id)
    to_user = User.objects.get(id=to_user_id)
    message = f"{from_user.full_name} has {status.lower()} your connection request."
    notification=Notification.objects.create(user=from_user, message=message)
    print(notification)
