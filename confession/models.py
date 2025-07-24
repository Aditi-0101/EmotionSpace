from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Confession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    confession = models.TextField()
    is_edited = models.BooleanField(default=False)
    hearts = models.ManyToManyField(User, related_name='liked_confessions', blank=True)

    def total_hearts(self):
        return self.hearts.count()
    
    def __str__(self):
        return f"{self.user.username}'s confession"