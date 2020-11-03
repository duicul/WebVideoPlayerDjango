from django.db import models
import json

# Create your models here.
class User_db(models.Model): 
   username = models.CharField(max_length = 100 , unique=True)
   password = models.CharField(max_length = 100)
   def getDict(self):
        return {"username":self.username,"password":self.password}

class Category_db(models.Model):
    category_path = models.CharField(max_length = 200 , unique=True)
    category_name = models.CharField(max_length = 30)
    
    def getDict(self):
        return {"category_path":self.category_path,"category_name":self.category_name}

class Movie_db(models.Model):
    name = models.CharField(max_length = 100)
    abs_path = models.CharField(max_length = 100 , unique=True )
    img_url = models.CharField(max_length = 100,default="")
    movie_title = models.CharField(max_length = 100,default="")
    movie_url = models.CharField(max_length = 100,default="")
    descr = models.TextField(default="")
    sub_json = models.CharField(max_length = 100,default="[]")
    unique_id = models.CharField(max_length = 100 , unique=True)
    category =  models.ForeignKey(Category_db, on_delete=models.CASCADE)
    
    
    def getDict(self):
        return {"movie_title":self.movie_title,"name":self.name,"abs_path":self.abs_path,"img_url":self.img_url,"movie_url":self.movie_url,"sub_json":self.sub_json,"unique_id":self.unique_id}
    
    def getDescHTML(self):
        return self.descr


class Show_db(models.Model):
    name = models.CharField(max_length = 100)
    abs_path = models.CharField(max_length = 100 , unique=True )
    movie_title = models.CharField(max_length = 100,default="")
    descr = models.TextField(default="")
    sub_json = models.CharField(max_length = 100,default="[]")
    unique_id = models.CharField(max_length = 100 , unique=True)
    img_url = models.CharField(max_length = 100,default="")
    category =  models.ForeignKey(Category_db, on_delete=models.CASCADE)
    
    def getDict(self):
        return {"movie_title":self.movie_title,"name":self.name,"abs_path":self.abs_path,"img_url":self.img_url,"sub_json":self.sub_json,"unique_id":self.unique_id}
    
    def getDescHTML(self):
        return self.descr

class Season_db(models.Model):
    name = models.CharField(max_length = 100)
    abs_path = models.CharField(max_length = 100 , unique=True )
    movie_title = models.CharField(max_length = 100,default="")
    descr = models.TextField(default="")
    unique_id = models.CharField(max_length = 100 , unique=True)
    show =  models.ForeignKey(Show_db, on_delete=models.CASCADE)
    img_url = models.CharField(max_length = 100,default="")
    
    def getDict(self):
        return {"movie_title":self.movie_title,"name":self.name,"abs_path":self.abs_path,"img_url":self.img_url,"unique_id":self.unique_id}
    
    def getDescHTML(self):
        return self.descr

class Episode_db(models.Model):
    name = models.CharField(max_length = 100)
    abs_path = models.CharField(max_length = 100 , unique=True )
    movie_title = models.CharField(max_length = 100,default="")
    movie_url = models.CharField(max_length = 100,default="")
    descr = models.TextField(default="")
    sub_json = models.CharField(max_length = 100,default="[]")
    unique_id = models.CharField(max_length = 100 , unique=True)
    season =  models.ForeignKey(Season_db, on_delete=models.CASCADE)
    
    
    def getDict(self):
        return {"movie_title":self.movie_title,"name":self.name,"abs_path":self.abs_path,"img_url":self.img_url,"movie_url":self.movie_url,"sub_json":self.sub_json,"unique_id":self.unique_id}
    
    def getDescHTML(self):
        return self.descr





