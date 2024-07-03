from django.db import models
from cloudinary.models import CloudinaryField


# Create your models here.
class About(models.Model):
    """
    Stores a single about me text
    """
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()
    profile_image = CloudinaryField('image', default='placeholder')

    def __str__(self):
        return self.title


class ContactUs(models.Model):
    """
    Stores a single contact request message
    """
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.name}"
