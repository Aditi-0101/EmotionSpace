from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=10,blank=True, choices=[
        ('Male','Male'),
        ('Female','Female'),
        ('Other','Other')
    ])
    dob = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    
    def _str_(self):
        return self.user.username