from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class Journal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    topic = models.CharField(max_length=100)
    entry = models.TextField()
    is_edited = models.BooleanField(default=False)
    date = models.DateField(default=timezone.now)
    joy = models.FloatField(null=True, blank=True)
    sad = models.FloatField(null=True, blank=True)
    neutral = models.FloatField(null=True, blank=True)
    ai_insight = models.JSONField(null=True, blank=True)
    
    def _str_(self):
        return self.topic