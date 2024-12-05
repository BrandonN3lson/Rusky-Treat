from django.db import models
from cloudinary.models import CloudinaryField


class About (models.Model):
    """
    Models for the About section of the Rusky Treats Django project.

    This module defines two models:
    1. `About`: Represents the About section content,
        including a title and rich text content.
    2. `AboutImages`: Represents images associated with the About section,
        stored using Cloudinary.

    Classes:
    About: Contains the title and content for the About section.
    AboutImages: Links images to an About instance and stores them in the  
                 'rusky_treat_images' folder on Cloudinary.

    """
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.title


class AboutImages (models.Model):
    """
    AboutImages: Links images to an About instance and stores them in the  
                 'rusky_treat_images' folder on Cloudinary.

    """
    about = models.ForeignKey(About, related_name="images",
                              on_delete=models.CASCADE
                              )
    images = CloudinaryField('image',
                             folder='rusky_treat_images',
                             default='placeholder'
                             )

    def _str_(self):
        return f'image for {self.about.title}'
