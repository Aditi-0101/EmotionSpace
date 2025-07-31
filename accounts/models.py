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
    avatar = models.CharField(max_length=200,default="https://cdn-icons-png.flaticon.com/512/9308/9308904.png")
    
    def _str_(self):
        return self.user.username