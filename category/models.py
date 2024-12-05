from django.db import models
from cloudinary.models import CloudinaryField
from django.utils.text import slugify


class Category(models.Model):
    """
    This model represents product categories, including a title, slug,
    featured image, and description. It also automatically generates
    a unique slug based on the title.

    Attributes:
        1. title (CharField): The name of the category, limited to 30
                              characters and must be unique.

        2. slug (SlugField): A unique identifier generated from the title.
        3. featured_image (CloudinaryField): An optional image for the
                                             category, stored in the
                                             'rusky_treat_images' folder
                                             on Cloudinary. Defaults to
                                             'placeholder'.

        4. description (TextField): A description of the category. Defaults to
                                "No description available".

    Methods:
        1. save(*args, **kwargs): Overrides the default save method to
                               auto-generate the slug from the title
                               if it doesn't already exist.
        2. __str__(): Returns the title of the category
                   as its string representation.
    """

    title = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    featured_image = CloudinaryField('image',
                                     folder='rusky_treat_images',
                                     default='placeholder'
                                     )
    description = models.TextField(default="No description available")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
