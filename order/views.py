from django.contrib.auth.decorators import login_required
from django.views import generic
from .models import Order


class OrderPage(generic.ListView):
    model = Order
    template_name = "order_page.html"
    context_object_name = "orders"


@login_required
def get_queryset(self):
    return Order.objects.filter(user=self.request.user, status="Pending")
