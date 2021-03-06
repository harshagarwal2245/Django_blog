from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField



class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')



class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250,verbose_name="Title")
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author= models.ForeignKey(User, related_name='blog_posts', on_delete=models.CASCADE,verbose_name="Author")
    body = RichTextField(verbose_name="Body")
    publish = models.DateTimeField(default=timezone.now,verbose_name="Publish")
    created = models.DateTimeField(auto_now_add=True,verbose_name="Created")
    updated = models.DateTimeField(auto_now=True,verbose_name="Updated")
    snippet = models.CharField(max_length=250,verbose_name="Snippet",)
    header = models.ImageField(blank=True,null=True,upload_to='blog/%Y/%m/%d',verbose_name="Header")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    users_like=models.ManyToManyField(User,related_name='post_likes',blank=True)

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    objects=models.Manager()    
    published=PublishedManager()
    tags=TaggableManager()

    
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('created',)
    
    
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
