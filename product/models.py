from django.db import models
from category.models import Category
from cloudinary.models import CloudinaryField
from django.utils.text import slugify


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    image = CloudinaryField('image',
                            folder='rusky_treat_images',
                            default='placeholder')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
