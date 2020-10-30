from django.db import models

# Create your models here.
class User_db(models.Model):
    user_name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    
class Video_File(models.Model):    
    full_path = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    ext = models.CharField(max_length=10)