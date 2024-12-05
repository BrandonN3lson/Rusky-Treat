from django.db import models
from category.models import Category
from cloudinary.models import CloudinaryField
from django.utils.text import slugify


class Product(models.Model):
    """
    Class: Product
    - Represents a product in the store.
      This model also includes methods for automatically generating slugs and
      formatting product information.

    Attributes:
    - name (CharField): The name of the product (max length 100).
    - slug (SlugField): A URL version of the product name, unique for
                        each product.
    - image (CloudinaryField): A field for storing product images via
                               Cloudinary.
                               The images are stored in the
                               'rusky_treat_images' folder, with a
                               placeholder image by default.
    - description (TextField): A detailed description of the product.
    - price (DecimalField): The price of the product with a maximum of 10
                            digits, and 2 decimal places.
    - category (ForeignKey): A reference to the `Category` model, representing
                             the category to which the product belongs.
    - created_on (DateTimeField): The timestamp when the product is created
                                  (auto-generated).
    - updated_on (DateTimeField): The timestamp when the product is last
                                  updated (auto-updated).

    Methods:
    - save: Overrides save method that automatically generates a slug based
            on the product name if the slug is not already set,
            ensuring unique URL slugs.
    - __str__: Returns the product's name as its string,
               which is used in the admin panel and when referencing the
               product.

    """

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
