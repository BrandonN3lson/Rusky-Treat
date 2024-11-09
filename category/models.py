from django.db import models
from cloudinary.models import CloudinaryField


class Category(models.Model):

    title = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    featured_image = CloudinaryField('image',
                                     folder='rusky_treat_images',
                                     default='placeholder'
                                     )
    description = models.TextField(default="No description available")

    def __str__(self):
        return self.title
