from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from cloudinary.models import CloudinaryField
from ckeditor.fields import RichTextField

class UserProfileManager(models.Manager):
    pass

class UserProfile(models.Model):
    #gender choice
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    #user = models.OneToOneField(User)
    user                     = models.OneToOneField(User, on_delete=models.CASCADE)
    description              = models.TextField(default='', null = True, blank = True)
    address                  = models.TextField(default='', null = True, blank = True)
    website                  = models.URLField(default='', null = True, blank = True)
    gender                   = models.CharField(max_length = 20, default = 'Male')
    mobileNumber             = models.IntegerField(default=0, null = True, blank = True)
    profilePic               = CloudinaryField('image', null = True, blank = True)
    coverPic                 = CloudinaryField('image', null = True, blank = True)
    #privacy
    contactDetailsVisible    = models.IntegerField(default = 0, null = True, blank = True)
    profileDetailsVisible    = models.IntegerField(default = 1, null = True, blank = True)
    #Fav
    fav_music                = models.CharField(max_length = 120, null = True, blank = True)
    fav_books                = models.CharField(max_length = 120, null = True, blank = True)
    fav_movie                = models.CharField(max_length = 120, null = True, blank = True)
    skills                   = models.CharField(max_length = 120, null = True, blank = True)
    interest                 = models.CharField(max_length = 120, null = True, blank = True)
    facebook_url             = models.URLField(max_length=200, null = True, blank = True)
    linkedin_url             = models.URLField(max_length=200, null = True, blank = True)
    twitter_url              = models.URLField(max_length=200, null = True, blank = True)
    instagram_url            = models.URLField(max_length=200, null = True, blank = True)
    


    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = UserProfile(user=user)
        user_profile.save()
post_save.connect(create_profile, sender=User)

