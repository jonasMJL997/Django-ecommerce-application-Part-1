from django.urls import path
from . import views

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/vendor/', views.register_vendor, name='register_vendor'),
    path('register/buyer/', views.register_buyer, name='register_buyer'),
    
    # Password reset
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('password-reset-confirm/<str:token>/', views.password_reset_confirm, name='password_reset_confirm'),
    
    # Product pages
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    
    # Vendor pages
    path('vendor/dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('vendor/stores/', views.store_list, name='store_list'),
    path('vendor/stores/create/', views.store_create, name='store_create'),
    path('vendor/stores/<int:store_id>/edit/', views.store_edit, name='store_edit'),
    path('vendor/stores/<int:store_id>/delete/', views.store_delete, name='store_delete'),
    path('vendor/products/', views.product_list, name='product_list'),
    path('vendor/products/create/', views.product_create, name='product_create'),
    path('vendor/products/<int:product_id>/edit/', views.product_edit, name='product_edit'),
    path('vendor/products/<int:product_id>/delete/', views.product_delete, name='product_delete'),
    
    # Buyer pages
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:product_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('product/<int:product_id>/review/', views.add_review, name='add_review'),
]





