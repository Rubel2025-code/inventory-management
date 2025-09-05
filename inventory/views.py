from .forms import CustomUserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Product
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required


@login_required
def product_list(request):
    products = Product.objects.all()
    context = {
        'products': products,  # ✅ Product list with real-time stock
        'is_admin': request.user.is_staff or request.user.is_superuser
    }
    return render(request, 'inventory/product_list.html', context)  # ✅ Use context

from django.shortcuts import render, redirect
from .models import Product
from django import forms

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'stock', 'price', 'supplier_name', 'supplier_contact', 'image']

@staff_member_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'inventory/add_product.html', {'form': form})
@staff_member_required
def edit_product(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'inventory/edit_product.html', {'form': form})
@staff_member_required
def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'inventory/delete_product.html', {'product': product})
import csv
from django.http import HttpResponse

def export_csv(request):
    products = Product.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name', 'Category', 'Quantity', 'Price', 'Added On'])

    for p in products:
        writer.writerow([p.name, p.category, p.stock, p.price, p.added_on])

    return response
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
        else:
            print("❌ Form errors:", form.errors)  # Debugging output
    else:
        form = CustomUserCreationForm()  # ✅ Use custom form here too
    return render(request, 'inventory/register.html', {'form': form})
