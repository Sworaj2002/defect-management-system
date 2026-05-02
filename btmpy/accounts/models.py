from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserData(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)

    #add extra fields
    Door_no=models.CharField(max_length=100)
    Street = models.CharField(max_length=100)
    City = models.CharField(max_length=100)
    State = models.CharField(max_length=200)
    Zipcode = models.IntegerField()
    Profile_pic = models.ImageField(upload_to='userimg',blank=True,null=True)