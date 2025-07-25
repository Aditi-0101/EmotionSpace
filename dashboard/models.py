from django.db import models
from django.contrib.auth.models import User

class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('confession', 'Confession'),
        ('journal', 'Journal'),
        ('like', 'Like'),
        ('comment', 'Comment'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    description = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.activity_type} at {self.timestamp.strftime("%Y-%m-%d %H:%M")}'