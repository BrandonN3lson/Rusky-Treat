from django.db import models
from cloudinary.models import CloudinaryField


class About (models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    
    def __str__(self):
        return self.title


class AboutImages (models.Model):
    about = models.ForeignKey(About, related_name="images",
                              on_delete=models.CASCADE
                              )
    images = CloudinaryField('image',
                             folder='rusky_treat_images',
                             default='placeholder'
                             )

    def _str_(self):
        return f'image for {self.about.title}'
