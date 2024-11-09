from django.db import models


class Category(models.Model):

    title = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.title
