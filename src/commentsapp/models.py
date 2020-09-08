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

#parent model
class forum(models.Model):
    # discuss = models.OneToOneField(Discussion, blank=True, null=True, on_delete=models.SET_NULL)
    # name=models.CharField(max_length=200,default="anonymous" )
    profile = models.ForeignKey(profile, null=True, blank=True,on_delete=models.SET_NULL)
    topic= models.CharField(max_length=300)
    description = models.CharField(max_length=1000,blank=True)
    link = models.CharField(max_length=100 ,null =True)
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    
    def __str__(self):
        return str(self.topic)
 
#child model
class Discussion(models.Model):
    user = models.ForeignKey(User, null=True, blank=True,on_delete=models.CASCADE)
    forum = models.ForeignKey(forum,blank=True, null=True, on_delete=models.CASCADE)
    discuss = models.CharField(max_length=1000)
 
    def __str__(self):
        return str(self.forum)