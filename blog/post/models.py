from __future__ import  unicode_literals
from django.db import models
from django.urls import reverse
from cloudinary.models import CloudinaryField
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.conf import settings
from time import gmtime, strftime
from django.http import request
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

from comments.models import Comment
from ckeditor_uploader.fields import RichTextUploadingField


class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(PostManager, self).filter(draft = False).filter(publish__lte = timezone.now())

    def all(self, *args, **kwargs):
        return super(PostManager, self).all()


class ContactAdmin(models.Model):
    name    = models.CharField( max_length=120 )
    emailid = models.EmailField(max_length=254)
    subject = models.CharField( max_length=120 )
    message = RichTextUploadingField()

    def __str__(self):
        return self.name

class BlogRequest(models.Model):
    author      = models.CharField(max_length = 120)
    userRequest = models.CharField(max_length = 150)
    created_on  = models.DateTimeField(auto_now=False, auto_now_add=True)
    
    def __str__(self):
        return self.author

class Post(models.Model):
    title           = models.CharField( max_length=120 )
    content         = RichTextUploadingField()
    slug            = models.SlugField(unique = True)
    image           = CloudinaryField('image', null = True, blank = True)
    image_caption   = models.CharField(max_length=100, blank=True, null = True)
    updated_on      = models.DateTimeField(auto_now=True, auto_now_add=False)
    created_on      = models.DateTimeField(auto_now=False, auto_now_add=True)
    author          = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.DO_NOTHING)
    tags            = models.CharField(max_length = 120, null = True, blank = True)
    category        = models.CharField(max_length = 120, null = True, blank = True)
    likes           = models.IntegerField(default=0)
    #dislikes       = models.IntegerField(default=0)
    draft           = models.BooleanField(default=0)
    publish         = models.DateField(auto_now=False, auto_now_add=False)

    objects         = PostManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"slug": self.slug})
    
    def get_update_url(self):
        return reverse("update-detail", kwargs={"slug": self.slug})
    
    @property
    def comments(self):
        instance = self
        qs       = Comment.objects.filter_by_instance(instance)
        return qs
    
    @property
    def commentsCount(self):
        instance    = self
        ccount      = Comment.objects.filter_by_instance(instance).count()
        return ccount

    @property
    def get_content_type(self):
        instance        = self
        content_type    = ContentType.objects.get_for_model(instance.__class__)
        return content_type

    @property
    def viewscount(self):
        instance    = self
        viewCount   = no_of_views.objects.get(post = instance).views
        return viewCount

class no_of_views(models.Model):
    post       = models.ForeignKey(Post, on_delete=models.CASCADE)
    views      = models.IntegerField(default=0)
    updated    = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.post.title

class UserPrefer(models.Model):
    user    = models.ForeignKey(settings.AUTH_USER_MODEL, default=1,on_delete=models.DO_NOTHING)
    Post    = models.ForeignKey(Post, on_delete=models.CASCADE)
    value   = models.IntegerField()
    date    = models.DateTimeField(auto_now=True, auto_now_add = False)

    def __str__(self):
        return str(self.user) + ':' + str(self.post) +':' + str(self.value)
    

def pre_save_slugify(sender, instance, *args, **kwargs):
    titleslug = slugify(instance.title)
    instance.slug = titleslug +  '-' + strftime("%Y%m%d-%H%M%S", gmtime())

pre_save.connect(pre_save_slugify, sender = Post)
