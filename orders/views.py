from inventory.models import Product
from django.views.decorators.http import require_POST
from django.contrib import messages  
from .models import Cart, CartItem, Order
from .forms import PaymentForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

@require_POST
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    quantity = int(request.POST.get('quantity', 1))

    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if created:
        item.quantity = quantity
    else:
        item.quantity += quantity
    item.save()

    return redirect('cart_view')

@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    total = sum(item.subtotal() for item in items)

    return render(request, 'orders/cart.html', {
        'items': items,
        'total': total,
    })


@login_required
def make_payment(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    total = sum(item.subtotal() for item in items)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            CartItem.objects.filter(cart__user=request.user).delete()
            return render(request, 'orders/payment_success.html')

        else:
            messages.error(request, 'Invalid payment form. Please try again.')
    else:
        form = PaymentForm()

    return render(request, 'orders/make_payment.html', {
        'form': form,
        'items': items,
        'total': total,
    })


@login_required
def admin_order_list(request):
    if not request.user.is_staff:
        return redirect('product_list')
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'orders/admin_orders.html', {'orders': orders})

@login_required
def update_order_status(request, order_id, status):
    if request.user.is_staff:
        order = get_object_or_404(Order, id=order_id)
        order.status = status
        order.save()
    return redirect('admin_order_list')
