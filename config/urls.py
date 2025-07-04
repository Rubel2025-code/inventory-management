from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
import inventory.views  # ✅ Make sure this is imported

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventory.urls')),
    path('cart/', include('orders.urls')),

    # 🔐 Auth
    path('register/', inventory.views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='inventory/login.html'), name='login'),

    # ✅ Updated logout to redirect to /login/
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
]
