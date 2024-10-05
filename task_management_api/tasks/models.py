from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    pass


class Task(models.Model):
    STATUS_CHOICES = [
        ('Todo', 'Todo'),
        ('In Progress', 'In Progress'),
        ('Done', 'Done')
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    priority = models.CharField(max_length=20)
    due_date = models.DateField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
