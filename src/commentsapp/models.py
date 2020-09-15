from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class profile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,default="anonymous")
    phone = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.name)

class Category(models.Model):
    category = models.CharField(max_length=200)

    def __str__(self):
        return self.category

#parent model
class forum(models.Model):
    # discuss = models.OneToOneField(Discussion, blank=True, null=True, on_delete=models.SET_NULL)
    # name=models.CharField(max_length=200,default="anonymous" )
    profile = models.ForeignKey(profile, null=True, blank=True,on_delete=models.SET_NULL)
    topic = models.CharField(max_length=300)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    description = models.CharField(max_length=1000,blank=True)
    num_comment = models.IntegerField(blank=True, null=True)
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    
    def __str__(self):
        return str(self.topic)
 
#child model
class Discussion(models.Model):
    user = models.ForeignKey(User, null=True, blank=True,on_delete=models.CASCADE)
    forum = models.ForeignKey(forum,blank=True, null=True, on_delete=models.CASCADE)
    discuss = models.CharField(max_length=1000)
    like = models.IntegerField(blank=True, null=True)
 
    def __str__(self):
        return str(self.discuss)