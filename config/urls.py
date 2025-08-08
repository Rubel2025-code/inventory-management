from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from inventory import views as inventory_views
from orders import views as order_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # App URLs
    path('', include('inventory.urls')),
    path('cart/', include('orders.urls')),

    # Auth routes
    path('register/', inventory_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='inventory/login.html'), name='login'),

    # ✅ Proper logout redirect to login page
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),


    # Remove cart item manually
    path('remove/<int:item_id>/', order_views.remove_cart_item, name='remove_cart_item'),
]
