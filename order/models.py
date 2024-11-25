from django.db import models
from django.contrib.auth.models import User
from product.models import Product


class Order(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="order"
                             )
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              default='Pending'
                              )

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


class OrderItem (models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              related_name='items'
                              )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10,
                                      decimal_places=2,
                                      default=0
                                      )

    @property
    def calculate_total_price(self):
        return self.product.price * self.quantity

    def save(self, *args, **kwargs):
        self.total_price = self.calculate_total_price
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"Order #{self.order.id} - "
            f"Product: {self.product.name} - "
            f"Qty: {self.quantity} - "
            f"Total_prices {self.total_price}"
         )
