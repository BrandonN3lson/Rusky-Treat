from .models import Order
from django.core.paginator import Paginator


def order_history_processor(request):
    orders = None

    if request.user.is_authenticated:
        if request.user.is_superuser:
            orders = Order.objects.all()
        else:
            orders = Order.objects.filter(user=request.user,
                                          status="Pending"
                                          )

    paginator = Paginator(orders, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    orders = page_obj

    return {
            'orders': orders
            }
