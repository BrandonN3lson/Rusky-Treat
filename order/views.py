from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic, View
from django.contrib import messages
from .models import Order, OrderItem, Product


class OrderPage(generic.ListView):
    model = Order
    template_name = "order_page.html"
    context_object_name = "orders"
    paginate_by = 3

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

        if product_id_str in cart:
            cart[product_id_str] += quantity
            messages.success(request,
                             f'Updated {product.name}'
                             f' quantity in your cart'
                             )
        elif product_id_str not in cart:
            cart[product_id_str] = quantity
            messages.success(request, f'{product.name} was added successfully')
        else:
            messages.error(request, f"Error adding {product.name} to cart")

        request.session['cart'] = cart
        return redirect('products')


class RemoveFromCart(View):

    def get(self, request, product_id):
        cart = request.session.get('cart', {})
        product = get_object_or_404(Product, id=product_id)
        product_id_str = str(product.id)

        if product_id_str in cart:
            del cart[product_id_str]

        request.session['cart'] = cart
        return redirect('orders')


class UpdateProductQuantity(View):

    def post(self, request, product_id):
        cart = request.session.get('cart', {})
        product = get_object_or_404(Product, id=product_id)
        product_id_str = str(product.id)
        quantity = int(request.POST.get('quantity', 1))

        if quantity > 0:
            cart[product_id_str] = quantity
            request.session['cart'] = cart
            return redirect('orders')
        else:
            del cart[product_id]
            request.session['cart'] = cart
            return redirect('orders')


class SubmitOrder(View):

    def post(self, request):
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, 'Your cart is empty')
            return redirect('orders')

        order = Order.objects.create(
            user=request.user,
            status='Pending',
        )

        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, id=product_id)
            order_item, created = OrderItem.objects.get_or_create(
                order=order,
                product=product,
                defaults={'quantity': quantity}
            )

        order.save()

        request.session['cart'] = {}
        messages.success(
                        request,
                        f"Your Order {order.id} was submitted successfully"
                        )
        return redirect('orders')


class EditOrder(View):

    def get(self, request, order_id):
        try:
            order = get_object_or_404(Order, id=order_id,
                                      user=request.user, status="Pending"
                                      )
        except Exception as e:
            print(f'Error fetching order {e}')
            messages.error(request, 'Order not found')
            return redirect('orders')

        if not order.user == request.user:
            editing_order = False
            messages.error('You are not authorised to edit this order')
            return redirect('orders')

        edit_cart = request.session['edit_cart'] = {}
        editing_order = True
        edit_cart = {
            str(item.product.id):
            item.quantity for item in order.items.all()
        }

        request.session['edit_cart'] = edit_cart

        order_items = []
        order_total_price = 0
        for product_id, quantity in edit_cart.items():
            product = Product.objects.get(id=product_id)
            item_total_price = product.price * quantity
            order_total_price += product.price * quantity
            order_items.append({
                'product': product,
                'quantity': quantity,
                'total_price': item_total_price,
                'order_total_price': order_total_price
            })

        return render(request, 'order_page.html', {
            'order': order,
            'product': product,
            'edit_cart': edit_cart,
            'order_items': order_items,
            'order_total_price': order_total_price,
            'editing_order': editing_order
            })


class RemoveFromOrder(View):

    def get(self, request, order_id, product_id):
        try:
            order = get_object_or_404(Order, id=order_id,
                                      user=request.user, status="Pending"
                                      )
        except Exception as e:
            print(f'Error fetching order {e}')
            messages.error(request, 'Order not found')
            return redirect('orders')

        edit_cart = request.session.get('edit_cart', {})
        print("before removing product:", request.session['edit_cart'])

        product = get_object_or_404(Product, id=product_id)
        product_id_str = str(product.id)
        if product_id_str in edit_cart:
            del edit_cart[product_id_str]
            request.session['edit_cart'] = edit_cart
            request.session.modified = True

        order_items = []
        item_total_price = 0
        order_total_price = 0
        for product_id, quantity in edit_cart.items():
            product = Product.objects.get(id=product_id)
            item_total_price = product.price * quantity
            order_total_price += product.price * quantity
            order_items.append({
                'product': product,
                'quantity': quantity,
                'total_price': item_total_price,
                'order_total_price': order_total_price
            })

        editing_order = True
        print("after removing product:", request.session['edit_cart'])

        return render(request, 'order_page.html', {
            'order': order,
            'product': product,
            'edit_cart': edit_cart,
            'order_items': order_items,
            'order_total_price': order_total_price,
            'editing_order': editing_order
            })


class UpdateOrderQuantity(View):

    def post(self, request, order_id, product_id):
        try:
            order = get_object_or_404(Order, id=order_id,
                                      user=request.user, status="Pending"
                                      )
        except Exception as e:
            print(f'Error fetching order {e}')
            messages.error(request, 'Order not found')
            return redirect('orders')

        edit_cart = request.session.get('edit_cart', {})
        product = get_object_or_404(Product, id=product_id)
        product_id_str = str(product.id)
        quantity = int(request.POST.get('quantity', 0))

        if quantity > 0:
            edit_cart[product_id_str] = quantity
            request.session['edit_cart'] = edit_cart
            editing_order = True
        else:
            del edit_cart[product_id]
            request.session['edit_cart'] = edit_cart
            editing_order = False
            return redirect('orders')

        order_items = []
        item_total_price = 0
        order_total_price = 0
        for product_id, quantity in edit_cart.items():
            product = Product.objects.get(id=product_id)
            item_total_price = product.price * quantity
            order_total_price += product.price * quantity
            order_items.append({
                'product': product,
                'quantity': quantity,
                'total_price': item_total_price,
                'order_total_price': order_total_price
            })

        request.session['edit_cart'] = edit_cart
        editing_order = True
        return render(request, 'order_page.html', {
            'order': order,
            'product': product,
            'edit_cart': edit_cart,
            'order_items': order_items,
            'order_total_price': order_total_price,
            'editing_order': editing_order
            })


class CancelEdit(View):

    def get(self, request, order_id):

        messages.success(request, "Editing canceled.")

        return redirect('orders')


class CancelOrder(View):
    def get(self, request, order_id):
        try:
            order = get_object_or_404(Order, id=order_id,
                                      user=request.user, status="Pending"
                                      )
        except Exception as e:
            print(f'Error fetching order {e}')
            messages.error(request, 'Order not found')
            return redirect('orders')
        order.status = 'Cancelled'
        order.save()
        messages.success(request, f'Your order {order.id} has been cancelled')
        return redirect('orders')


class ResubmitOrder(View):

    def post(self, request, order_id):
        try:
            order = get_object_or_404(Order, id=order_id,
                                      user=request.user, status="Pending"
                                      )
        except Exception as e:
            print(f'Error fetching order {e}')
            messages.error(request, 'Order not found')
            return redirect('orders')

        edit_cart = request.session.get('edit_cart', {})
        if not edit_cart:
            messages.error(request, 'you have no items in order')
            return redirect('orders')

        for product_id, quantity in edit_cart.items():
            product = get_object_or_404(Product, id=product_id)
            order_item, created = OrderItem.objects.get_or_create(
                order=order,
                product=product,
            )
            if not created:
                order_item.quantity = quantity
                order_item.save()

        for item in order.items.all():
            if str(item.product.id) not in edit_cart:
                item.delete()

        order.save()
        request.session['edit_cart'] = {}
        messages.success(request,
                         f"Your Order {order.id} was edited successfully.")

        return redirect('orders')
