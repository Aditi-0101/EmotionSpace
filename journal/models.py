from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Journal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    topic = models.CharField(max_length=100)
    entry = models.TextField()
    is_edited = models.BooleanField(default=False)
    
    def _str_(self):
        return self.topic