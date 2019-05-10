from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Entry(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(default=datetime.now)
    creator = models.ForeignKey(User)
    
    def __unicode__(self):
	    return self.title
    
    class Meta:
        verbose_name_plural = "Entries"

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    photo  = models.ImageField(upload_to="photos", null=True, blank=True)
    country = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = "User Profiles"       

class Comment(models.Model):
    created = models.DateTimeField(default=datetime.now)
    author = models.ForeignKey(User)
    body = models.TextField()
    post = models.ForeignKey(Entry)

    def __unicode__(self):
        return unicode("%s: %s" % (self.post , self.body[:60])) 
