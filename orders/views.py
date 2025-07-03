from django.shortcuts import render, redirect, get_object_or_404
from inventory.models import Product
from .models import Cart, CartItem
from django.contrib.auth.decorators import login_required

from django.views.decorators.http import require_POST

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
