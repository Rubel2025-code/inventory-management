from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from inventory import views as inventory_views  # if not already imported
from django.urls import path
from orders import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventory.urls')),
    path('cart/', include('orders.urls')),

    path('register/', inventory_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='inventory/login.html'), name='login'),

    # ✅ Updated LogoutView with GET allowed
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
]
