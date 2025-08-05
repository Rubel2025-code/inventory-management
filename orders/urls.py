from django.urls import path
from . import views

urlpatterns = [
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('make-payment/', views.make_payment, name='make_payment'),
    path('admin-orders/', views.admin_order_list, name='admin_order_list'),
    path('update-order-status/<int:order_id>/<str:status>/', views.update_order_status, name='update_order_status'),
    path("remove/<int:item_id>/", views.remove_cart_item, name="remove_cart_item"),

]
