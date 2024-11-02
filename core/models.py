from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class ContactMessage(models.Model):
    user_name = models.CharField(max_length=255)
    user_email = models.EmailField()
    mobile_number = models.CharField(max_length=20)
    subject = models.CharField(max_length=255)
    user_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.user_name} ({self.user_email})'