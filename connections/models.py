from django.db import models
from django.conf import settings


# Create your models here.

class Connection(models.Model):
  class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        REJECTED = 'REJECTED', 'Rejected'


  from_user=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='sent_requests',on_delete=models.CASCADE)
  to_user=models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_requests', on_delete=models.CASCADE)
  status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )
  created_at= models.DateTimeField(auto_now_add=True)

  class Meta:
    unique_together=('from_user','to_user')

  def __str__(self):
    return f'{self.from_user} -> {self.to_user} ({self.status})'
