from django.db import models
import json

# Create your models here.
class User_db(models.Model): 
   username = models.CharField(max_length = 100 , unique=True)
   password = models.CharField(max_length = 100)
   def getDict(self):
        return {"username":self.username,"password":self.password}

class Movie_db(models.Model):
    name = models.CharField(max_length = 100)
    abs_path = models.CharField(max_length = 100 , unique=True )
    img_url = models.CharField(max_length = 100)
    movie_url = models.CharField(max_length = 100)
    desc_url = models.CharField(max_length = 100)
    sub_json = models.CharField(max_length = 100)
    unique_id = models.CharField(max_length = 100 , unique=True)
    
    def getDict(self):
        return {"name":self.name,"abs_path":self.abs_path,"img_url":self.img_url,"movie_url":self.movie_url,"desc_url":self.desc_url,"sub_json":self.sub_json,"unique_id":self.unique_id}