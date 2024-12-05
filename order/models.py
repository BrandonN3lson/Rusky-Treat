from django.db import models
from django.contrib.auth.models import User
from product.models import Product


class Order(models.Model):
    """
    Represents a customer order, including the user who placed it, the order
    date, and its current status. Each order can have multiple related
    `OrderItem` instances.

    Attributes:
    1. id (AutoField): Primary key for the order.
    2. user (ForeignKey): Links the order to the `User` who placed it.
    3. order_date (DateTimeField): Automatically records the date and
                                time the order was placed.
    4. status (CharField): Indicates the current status of the order.
                        Options are "Pending", "Processing", "Completed",
                        and "Cancelled". Defaults to "Pending".

    Meta:
        ordering: Orders are displayed in descending order of their order date.

    Properties:
        total_price: Calculates the total price of all `OrderItem` instances
                     related to this order.

    Methods:
        __str__(): Returns a string representation of the order,
                   including its ID and the username of the associated user.

    """

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
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

    class Meta:
        ordering = ["-order_date"]

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


class OrderItem (models.Model):
    """
    OrderItem Model.

    Represents an individual item within an order, including the product,
    quantity, and total price for the item.

    Attributes:
        1. id (AutoField): Primary key for the order item.
        2. order (ForeignKey): Links the item to its parent `Order`.
        3. product (ForeignKey): Links the item to the `Product`
                                 being purchased.
        4. quantity (PositiveIntegerField): Specifies the quantity of the
                                            product in the order.
                                            Defaults to 1.
        5. total_price (DecimalField): The total cost of this item,
                                       calculated as `product.price * quantity`

    Properties:
        calculate_total_price: Dynamically calculates the total price of the
                               item based on the product price and quantity.

    Methods:
        save(*args, **kwargs): Overrides the default save method
                               to calculate and set the `total_price`
                               before saving the instance.
        __str__(): Returns a string representation of the order item,
                   including the order ID, product name, quantity,
                   and total price.
    """

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
