from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic, View
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Order, OrderItem, Product


def calculate_cart(cart):
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
    return cart_items, item_total_price, cart_total_price


def calculate_order(edit_cart):
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
    return order_items, item_total_price, order_total_price


class AdminOrderPage(generic.ListView):
    """
    Class: AdminOrderPage
    Displays a list of all orders for the admin user, with pagination.
    Filters orders by status 'Pending' for pending orders and allows
    navigation through the order list. Only accessible by superusers.

    Attributes:
    - model: The model used for the list view (Order).
    - template_name: The template to render the page ("admin_order_page.html").
    - context_object_name: The name of the context to use in the
                           template ("admin_orders").

    Methods:
    - get_queryset: Filters and retrieves all orders or pending orders
                    based on the user's permissions.
    - get_context_data: Paginates the pending orders, filters orders by their
                        status, and adds context data.
    """

    model = Order
    template_name = "admin_order_page.html"
    context_object_name = "admin_orders"

    def get_queryset(self):

        admin_orders = Order.objects.all()

        if self.request.user.is_superuser:
            return admin_orders
        return Order.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # pagination for pending orders
        pending_orders = self.get_queryset().filter(status='Pending')
        paginator = Paginator(pending_orders, 2)
        page = self.request.GET.get('page')
        context['pending_orders'] = paginator.get_page(page)

        context[
            'processing_orders'
            ] = self.get_queryset().filter(status='Processing')

        return context


class ChangeOrderStatus(View):
    """
    Class: ChangeOrderStatus
    Handles the change of an order's status
    (Processing, Completed, or Cancelled).
    Displays a success or error message based on the new status
    and redirects to the admin orders page.

    Methods:
    - post: Updates the order's status and provides feedback to the admin,
            then redirects to 'admin_orders'.
    """

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        status = request.POST.get('status')

        order.status = status
        order.save()

        if status == 'Processing':
            messages.success(request, f'order #{order.id} in progress')
        elif status == 'Completed':
            messages.success(request, f'order #{order.id} Completed')
        elif status == 'Cancelled':
            messages.error(request, f'order #{order.id} Cancelled')

        return redirect('admin_orders')


class OrderPage(generic.ListView):
    """
    Class: OrderPage:
    - Displays a list of the current user's past orders with pagination
      and cart details. Also shows the user's cart items and their total price,
      if they are authenticated.

    Attributes:
    - model: The model used for the list view (Order).
    - template_name: The template to render the page ("order_page.html").
    - context_object_name: The name of the context to use in the template
                           ("orders").

    Methods:
    - get_queryset: Retrieves all orders placed by the authenticated user.
    - get_context_data: Retrieves the user's cart and order history, paginates
                        orders, and adds them to the context.
    """

    model = Order
    template_name = "order_page.html"
    context_object_name = "orders"

    def get_queryset(self):

        user_orders = Order.objects.filter(user=self.request.user).all()

        if self.request.user.is_authenticated:
            return user_orders
        else:
            return Order.objects.none()

    def get_context_data(self, **kwargs):

        # get items in cart and render to cart
        context = super().get_context_data(**kwargs)

        cart = self.request.session.get('cart', {})
        cart_items, cart_total_price, item_total_price = calculate_cart(cart)

        history_orders = self.get_queryset().all()
        paginator = Paginator(history_orders, 3)
        page_number = self.request.GET.get('page', 1)
        context['history_orders'] = paginator.get_page(page_number)

        context['cart_items'] = cart_items
        context['total_price'] = item_total_price
        context['cart_total_price'] = cart_total_price

        return context


class AddToCart(View):
    """
    Class: AddToCart
    - Handles the process of adding a product to the session cart.
      If the product already exists in the cart, its quantity is updated, else
      the product is added to the cart with the specified quantity.
      Displays a success message after adding or updating the product.

    Methods:
    - post: Adds or updates the product in the cart and redirects to the
            'products' page.
    """
    ...

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
    """
    Class: RemoveFromCart
    - Removes a product from the session cart.
      Redirects the user to the orders page after the product is removed.

    Methods:
    - get: Removes the specified product from the cart and redirects to
      the 'orders' page.
    """

    def get(self, request, product_id):
        cart = request.session.get('cart', {})
        product = get_object_or_404(Product, id=product_id)
        product_id_str = str(product.id)

        if product_id_str in cart:
            del cart[product_id_str]

        request.session['cart'] = cart
        return redirect('orders')


class UpdateProductQuantity(View):
    """
    Class: UpdateProductQuantity
    - Updates the quantity of a product in the session cart.
    """

    def post(self, request, product_id):
        cart = request.session.get('cart', {})
        product = get_object_or_404(Product, id=product_id)
        product_id_str = str(product.id)
        quantity = int(request.POST.get('quantity', 1))

        if quantity > 0:
            cart[product_id_str] = quantity
            request.session['cart'] = cart
            return redirect('orders')


class SubmitOrder(View):
    """
    Class: SubmitOrder
    - Submits a new order based on the products in the session cart.
      Creates an Order object and corresponding OrderItem objects for each
      product in the cart. Clears the cart after the order is successfully
      created and displays a success message.

    Methods:
    - post: Submits the order and clears the cart after the order is
            successfully placed.
    """

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
    """
    Class: EditOrder
    - Allows the user to edit an existing pending order's items.
      Retrieves the order items, loads them into the session cart,
      and calculates the new order totals. Renders the order page with
      the updated cart and items.

    Methods:
    - get: Loads the order's items into the session cart for
           editing and renders the updated order page.
    """

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
        (
            order_items,
            item_total_price,
            order_total_price
         ) = calculate_order(edit_cart)

        return render(request, 'order_page.html', {
            'order': order,
            'edit_cart': edit_cart,
            'order_items': order_items,
            'order_total_price': order_total_price,
            'editing_order': editing_order
            })


class RemoveFromOrder(View):
    """
    Class: RemoveFromOrder
    - Removes a product from an existing pending order.
      If the cart becomes empty after removal, the order status is set to
      'Cancelled', and a message is displayed.
      Otherwise, the updated order and cart details are displayed.

    Methods:
    - get: Removes the specified product from the order and updates the order
           status if necessary.
    """

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

        product = get_object_or_404(Product, id=product_id)
        product_id_str = str(product.id)
        if product_id_str in edit_cart:
            del edit_cart[product_id_str]
            request.session['edit_cart'] = edit_cart

        if not edit_cart:
            order.status = 'Cancelled'
            order.save()
            editing_order = False
            messages.info(request, f'Order {order.id} has been cancelled,'
                          f' because all items were removed')
            return redirect('orders')

        (
            order_items,
            item_total_price,
            order_total_price
         ) = calculate_order(edit_cart)

        editing_order = True
        return render(request, 'order_page.html', {
            'order': order,
            'product': product,
            'edit_cart': edit_cart,
            'order_items': order_items,
            'order_total_price': order_total_price,
            'editing_order': editing_order
            })


class UpdateOrderQuantity(View):
    """
    Class: UpdateOrderQuantity
    - Updates the quantity of a product in a pending order.
      Renders the updated order details after the change.

    Methods:
    - post: Updates the product from the order
            based on the specified quantity.
    """

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

        (
            order_items,
            item_total_price,
            order_total_price
         ) = calculate_order(edit_cart)

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
    """
    Class: CancelEdit
    - Cancels the editing of an order, discarding any changes made to the
      order's items.
      Redirects the user back to the orders page with a success message.

    Methods:
    - get: Cancels the editing process and redirects the user
    """

    def get(self, request, order_id):

        messages.success(request, "Editing canceled.")

        return redirect('orders')


class CancelOrder(View):
    """
    Class: CancelOrder
    - Cancels a pending order by changing its status to 'Cancelled'.
      Displays a success message and redirects the user to the orders page.

    Methods:
    - get: Cancels the specified order and redirects the user.
    """

    def get(self, request, order_id):
        try:
            order = get_object_or_404(Order, id=order_id,
                                      user=request.user, status="Pending"
                                      )
        except Exception as e:
            print(f'Error fetching order {e}')
            messages.error(request, 'Order was already cancelled')
            return redirect('orders')
        order.status = 'Cancelled'
        order.save()
        messages.success(request, f'Your order {order.id} has been cancelled')
        return redirect('orders')


class ResubmitOrder(View):
    """
    Class: ResubmitOrder
    - Allows the user to resubmit an edited pending order by updating the order
      items based on the current cart contents.
      Deletes any items from the original order that are no longer in the cart,
      and updates the quantity of items still in the cart.
      Displays a success message after resubmitting the order and clears the
      cart.

    Methods:
    - post: Resubmits the order with the updated items from the cart
            and clears the session cart.
    """

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
