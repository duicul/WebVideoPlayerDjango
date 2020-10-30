from django.db import models

# Create your models here.
class User_db(models.Model): 
   username = models.CharField(max_length = 100 , unique=True)
   password = models.CharField(max_length = 100)


class Movie(models.Model):
    name = models.CharField(max_length = 100)
    abs_path = models.CharField(max_length = 100 , unique=True )
    img_url = models.CharField(max_length = 100)
    video_url = models.CharField(max_length = 100)
    desc_url = models.CharField(max_length = 100)
    sub_json = models.CharField(max_length = 100)
    unique_id = models.CharField(max_length = 100 , unique=True)