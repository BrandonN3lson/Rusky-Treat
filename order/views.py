from django.shortcuts import get_object_or_404, redirect
from django.views import generic, View
from .models import Order, Product


class OrderPage(generic.ListView):
    model = Order
    template_name = "order_page.html"
    context_object_name = "orders"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.all()
        else:
            return Order.objects.filter(user=self.request.user,
                                        status="Pending")

    def get_context_data(self, **kwargs):

        # get items in cart and render to cart
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get('cart', {})

        cart_items = []
        item_total_price = 0
        cart_total_price = 0
        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
            item_total_price = product.price * quantity
            cart_total_price += product.price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total_price': item_total_price,
                'cart_total_price': cart_total_price
            })

        context['cart_items'] = cart_items
        context['total_price'] = item_total_price
        context['cart_total_price'] = cart_total_price

        return context


class AddToCart(View):

    # adding to 'cart' session
    def post(self, request, product_id):
        cart = request.session.get('cart', {})
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        product_id_str = str(product.id)

        print(f"Adding {quantity} of {product.name} to the cart.")
        print(f"Cart before adding: {cart}")

        if product_id_str in cart:
            cart[product_id_str] += quantity
        else:
            cart[product_id_str] = quantity

        request.session['cart'] = cart
        return redirect('orders')


class RemoveFromCart(View):

    def get(self, request, product_id):
        cart = request.session.get('cart', {})
        product = get_object_or_404(Product, id=product_id)
        product_id_str = str(product.id)

        if product_id_str in cart:
            if cart[product_id_str] > 1:
                cart[product_id_str] -= 1
            else:
                del cart[product_id_str]

        request.session['cart'] = cart
        return redirect('orders')
