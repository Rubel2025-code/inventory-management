from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from inventory.models import Product
from .models import Cart, CartItem, Order
from .forms import PaymentForm

# ✅ Add to Cart
@require_POST
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        quantity = int(request.POST.get("quantity", 1))
    except (ValueError, TypeError):
        quantity = 1

    if quantity <= 0:
        quantity = 1

    # check stock first
    if product.stock < quantity:
        messages.error(request, f"❌ Not enough stock for {product.name}. Only {product.stock} left.")
        return redirect("product_list")

    cart, _ = Cart.objects.get_or_create(user=request.user)

    # IMPORTANT: Provide defaults so DB insert includes a non-null quantity
    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )

    if not created:
        # if already exists, ensure adding quantity won't exceed stock
        if product.stock < item.quantity + quantity:
            messages.error(request, f"❌ Cannot add more than available stock for {product.name}.")
            return redirect("product_list")
        item.quantity += quantity
        item.save()
    else:
        # created with defaults already saved
        pass

    messages.success(request, f"✅ Added {quantity} × {product.name} to cart.")
    return redirect("cart_view")


# ✅ View Cart
@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    total = sum(item.subtotal() for item in items)

    return render(request, "orders/cart.html", {
        "items": items,
        "total": total
    })


# ✅ Remove Cart Item
@login_required
def remove_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    messages.success(request, "🗑️ Item removed from cart.")
    return redirect("cart_view")


# ✅ Make Payment
@login_required
def make_payment(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items:
        messages.error(request, "❌ Your cart is empty.")
        return redirect("product_list")

    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            transaction_number = form.cleaned_data["transaction_number"]

            # Create Order
            order = Order.objects.create(
                user=request.user,
                transaction_number=transaction_number
            )
            order.items.set(cart_items)

            # Deduct stock
            for item in cart_items:
                if item.product.stock >= item.quantity:
                    item.product.stock -= item.quantity
                    item.product.save()
                else:
                    messages.error(request, f"❌ Not enough stock for {item.product.name}.")
                    return redirect("cart_view")

            order.save()

            # Clear cart
            cart_items.delete()

            return render(request, "orders/payment_success.html", {"order": order})
    else:
        form = PaymentForm()

    total = sum(item.subtotal() for item in cart_items)
    return render(request, "orders/make_payment.html", {
        "form": form,
        "items": cart_items,
        "total": total
    })


# ✅ Admin Order List
@login_required
def admin_order_list(request):
    if not request.user.is_staff:
        return redirect("product_list")
    orders = Order.objects.all().order_by("-created_at")
    return render(request, "orders/admin_orders.html", {"orders": orders})


# ✅ Update Order Status
@login_required
def update_order_status(request, order_id, status):
    if request.user.is_staff:
        order = get_object_or_404(Order, id=order_id)
        order.status = status
        order.save()
        messages.success(request, f"✅ Order for {order.user.username} marked as {status}.")
    return redirect('admin_order_list')  # ✅ Always stay on the admin orders page

