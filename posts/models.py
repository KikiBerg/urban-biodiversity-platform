from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.utils.text import slugify
from .constants import STATUS_CHOICES, COMMENT_STATUS_CHOICES


# Create your models here.

class Category(models.Model):
    """
    Represents a category for blog posts.
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)   


    def __str__(self):
        return self.name


class Post(models.Model):
    """
    Represents a blog post.
    """
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    featured_image = CloudinaryField('image', default='placeholder')
    content = models.TextField()   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    excerpt = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        """
        Custom save method to automatically generate a slug from the post title.
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    Represents a comment on a blog post.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=COMMENT_STATUS_CHOICES, default='pending')

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'

