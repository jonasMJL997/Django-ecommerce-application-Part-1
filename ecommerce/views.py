from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import User, Store, Product, Order, OrderItem, Review, PasswordResetToken
from .forms import (
    VendorRegistrationForm, BuyerRegistrationForm, 
    StoreForm, ProductForm, ReviewForm, PasswordResetForm, PasswordResetConfirmForm
)


def home(request):
    """Home page showing all products"""
    products = Product.objects.filter(stock_quantity__gt=0).select_related('store')
    stores = Store.objects.all()
    
    # Get cart count for authenticated buyers
    cart_count = 0
    if request.user.is_authenticated and request.user.is_buyer():
        cart = request.session.get('cart', {})
        cart_count = sum(cart.values())
    
    context = {
        'products': products,
        'stores': stores,
        'cart_count': cart_count,
    }
    return render(request, 'ecommerce/home.html', context)


def register_vendor(request):
    """Vendor registration"""
    if request.method == 'POST':
        form = VendorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = User.VENDOR
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
    else:
        form = VendorRegistrationForm()
    return render(request, 'ecommerce/register_vendor.html', {'form': form})


def register_buyer(request):
    """Buyer registration"""
    if request.method == 'POST':
        form = BuyerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = User.BUYER
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
    else:
        form = BuyerRegistrationForm()
    return render(request, 'ecommerce/register_buyer.html', {'form': form})


def login_view(request):
    """User login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                
                # Redirect based on role
                if user.is_vendor():
                    return redirect('vendor_dashboard')
                else:
                    return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        except User.DoesNotExist:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'ecommerce/login.html')


def logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


@login_required
def vendor_dashboard(request):
    """Vendor dashboard"""
    if not request.user.is_vendor():
        messages.error(request, 'Access denied. Vendor access required.')
        return redirect('home')
    
    stores = Store.objects.filter(vendor=request.user)
    total_products = Product.objects.filter(store__vendor=request.user).count()
    
    context = {
        'stores': stores,
        'total_products': total_products,
    }
    return render(request, 'ecommerce/vendor_dashboard.html', context)


@login_required
def store_list(request):
    """List all stores for vendor"""
    if not request.user.is_vendor():
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    stores = Store.objects.filter(vendor=request.user)
    return render(request, 'ecommerce/store_list.html', {'stores': stores})


@login_required
def store_create(request):
    """Create a new store"""
    if not request.user.is_vendor():
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            store = form.save(commit=False)
            store.vendor = request.user
            store.save()
            messages.success(request, 'Store created successfully!')
            return redirect('store_list')
    else:
        form = StoreForm()
    return render(request, 'ecommerce/store_form.html', {'form': form, 'title': 'Create Store'})


@login_required
def store_edit(request, store_id):
    """Edit a store"""
    if not request.user.is_vendor():
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    store = get_object_or_404(Store, id=store_id, vendor=request.user)
    
    if request.method == 'POST':
        form = StoreForm(request.POST, instance=store)
        if form.is_valid():
            form.save()
            messages.success(request, 'Store updated successfully!')
            return redirect('store_list')
    else:
        form = StoreForm(instance=store)
    return render(request, 'ecommerce/store_form.html', {'form': form, 'title': 'Edit Store', 'store': store})


@login_required
def store_delete(request, store_id):
    """Delete a store"""
    if not request.user.is_vendor():
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    store = get_object_or_404(Store, id=store_id, vendor=request.user)
    
    if request.method == 'POST':
        store.delete()
        messages.success(request, 'Store deleted successfully!')
        return redirect('store_list')
    
    return render(request, 'ecommerce/store_confirm_delete.html', {'store': store})


@login_required
def product_list(request):
    """List all products for vendor"""
    if not request.user.is_vendor():
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    products = Product.objects.filter(store__vendor=request.user).select_related('store')
    return render(request, 'ecommerce/product_list.html', {'products': products})


@login_required
def product_create(request):
    """Create a new product"""
    if not request.user.is_vendor():
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    stores = Store.objects.filter(vendor=request.user)
    
    if not stores.exists():
        messages.warning(request, 'Please create a store first before adding products.')
        return redirect('store_create')
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        form.fields['store'].queryset = stores
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Product created successfully!')
            return redirect('product_list')
    else:
        form = ProductForm()
        form.fields['store'].queryset = stores
    
    return render(request, 'ecommerce/product_form.html', {'form': form, 'title': 'Create Product'})


@login_required
def product_edit(request, product_id):
    """Edit a product"""
    if not request.user.is_vendor():
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    product = get_object_or_404(Product, id=product_id, store__vendor=request.user)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        form.fields['store'].queryset = Store.objects.filter(vendor=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
        form.fields['store'].queryset = Store.objects.filter(vendor=request.user)
    
    return render(request, 'ecommerce/product_form.html', {'form': form, 'title': 'Edit Product', 'product': product})


@login_required
def product_delete(request, product_id):
    """Delete a product"""
    if not request.user.is_vendor():
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    product = get_object_or_404(Product, id=product_id, store__vendor=request.user)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('product_list')
    
    return render(request, 'ecommerce/product_confirm_delete.html', {'product': product})


def product_detail(request, product_id):
    """Product detail page with reviews"""
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)
    
    # Check if user has purchased this product
    has_purchased = False
    if request.user.is_authenticated:
        has_purchased = OrderItem.objects.filter(
            order__buyer=request.user,
            product=product
        ).exists()
    
    # Check if user has already reviewed
    user_review = None
    if request.user.is_authenticated:
        try:
            user_review = Review.objects.get(product=product, user=request.user)
        except Review.DoesNotExist:
            pass
    
    context = {
        'product': product,
        'reviews': reviews,
        'has_purchased': has_purchased,
        'user_review': user_review,
    }
    return render(request, 'ecommerce/product_detail.html', context)


@login_required
def add_to_cart(request, product_id):
    """Add product to cart"""
    if not request.user.is_buyer():
        messages.error(request, 'Only buyers can add items to cart.')
        return redirect('home')
    
    product = get_object_or_404(Product, id=product_id)
    
    if not product.is_in_stock():
        messages.error(request, 'Product is out of stock.')
        return redirect('product_detail', product_id=product_id)
    
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    
    current_quantity = cart.get(product_id_str, 0)
    new_quantity = current_quantity + 1
    
    if new_quantity > product.stock_quantity:
        messages.error(request, f'Only {product.stock_quantity} items available in stock.')
        return redirect('product_detail', product_id=product_id)
    
    cart[product_id_str] = new_quantity
    request.session['cart'] = cart
    messages.success(request, f'{product.name} added to cart!')
    
    return redirect('cart')


@login_required
def cart(request):
    """View shopping cart"""
    if not request.user.is_buyer():
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
            if product.is_in_stock():
                item_total = product.price * quantity
                total += item_total
                cart_items.append({
                    'product': product,
                    'quantity': quantity,
                    'total': item_total,
                })
            else:
                # Remove out of stock items
                del cart[product_id]
        except Product.DoesNotExist:
            # Remove non-existent products
            del cart[product_id]
    
    request.session['cart'] = cart
    request.session.modified = True
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'ecommerce/cart.html', context)


@login_required
def update_cart(request, product_id):
    """Update cart item quantity"""
    if not request.user.is_buyer():
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 0))
    
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    
    if quantity <= 0:
        cart.pop(product_id_str, None)
        messages.success(request, 'Item removed from cart.')
    elif quantity > product.stock_quantity:
        messages.error(request, f'Only {product.stock_quantity} items available.')
    else:
        cart[product_id_str] = quantity
        messages.success(request, 'Cart updated.')
    
    request.session['cart'] = cart
    request.session.modified = True
    
    return redirect('cart')


@login_required
def remove_from_cart(request, product_id):
    """Remove item from cart"""
    if not request.user.is_buyer():
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        product = Product.objects.get(id=product_id)
        del cart[product_id_str]
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, f'{product.name} removed from cart.')
    
    return redirect('cart')


@login_required
def checkout(request):
    """Checkout process"""
    if not request.user.is_buyer():
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    cart = request.session.get('cart', {})
    
    if not cart:
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart')
    
    # Validate cart and stock
    cart_items = []
    total = 0
    errors = []
    
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
            if not product.is_in_stock():
                errors.append(f'{product.name} is out of stock.')
                continue
            if quantity > product.stock_quantity:
                errors.append(f'Only {product.stock_quantity} {product.name} available.')
                continue
            
            item_total = product.price * quantity
            total += item_total
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': item_total,
            })
        except Product.DoesNotExist:
            errors.append(f'Product with ID {product_id} no longer exists.')
    
    if errors:
        for error in errors:
            messages.error(request, error)
        return redirect('cart')
    
    # Create order
    order = Order.objects.create(
        buyer=request.user,
        total_amount=total
    )
    
    # Create order items and update stock
    invoice_items = []
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item['product'],
            quantity=item['quantity'],
            price=item['product'].price
        )
        
        # Update stock
        item['product'].stock_quantity -= item['quantity']
        item['product'].save()
        
        invoice_items.append(item)
    
    # Clear cart
    request.session['cart'] = {}
    request.session.modified = True
    
    # Send invoice email
    try:
        send_invoice_email(request.user, order, invoice_items)
        order.invoice_sent = True
        order.save()
        messages.success(request, 'Order placed successfully! Invoice sent to your email.')
    except Exception as e:
        messages.warning(request, f'Order placed successfully, but email could not be sent: {str(e)}')
    
    return redirect('order_detail', order_id=order.id)


def send_invoice_email(user, order, items):
    """Send invoice email to user"""
    subject = f'Invoice for Order #{order.id}'
    
    message = f"""
    Thank you for your purchase!
    
    Order Number: #{order.id}
    Date: {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}
    
    Items:
    """
    
    for item in items:
        message += f"\n- {item['product'].name} x{item['quantity']} @ ${item['product'].price} = ${item['total']}"
    
    message += f"\n\nTotal: ${order.total_amount}"
    message += "\n\nThank you for shopping with us!"
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@ecommerce.com',
        [user.email],
        fail_silently=False,
    )


@login_required
def order_detail(request, order_id):
    """View order details"""
    order = get_object_or_404(Order, id=order_id, buyer=request.user)
    return render(request, 'ecommerce/order_detail.html', {'order': order})


@login_required
def add_review(request, product_id):
    """Add or update a review"""
    if not request.user.is_buyer():
        messages.error(request, 'Only buyers can leave reviews.')
        return redirect('home')
    
    product = get_object_or_404(Product, id=product_id)
    
    # Check if user has purchased (for verified review)
    has_purchased = OrderItem.objects.filter(
        order__buyer=request.user,
        product=product
    ).exists()
    
    # Check if review already exists
    review, created = Review.objects.get_or_create(
        product=product,
        user=request.user,
        defaults={'is_verified': has_purchased}
    )
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.is_verified = has_purchased
            review.save()
            messages.success(request, 'Review submitted successfully!')
            return redirect('product_detail', product_id=product_id)
    else:
        form = ReviewForm(instance=review)
    
    return render(request, 'ecommerce/review_form.html', {
        'form': form,
        'product': product,
        'has_purchased': has_purchased,
    })


def password_reset_request(request):
    """Request password reset"""
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                token_obj = PasswordResetToken.generate_token(user)
                
                # Send reset email
                reset_url = request.build_absolute_uri(
                    f'/password-reset-confirm/{token_obj.token}/'
                )
                
                send_mail(
                    'Password Reset Request',
                    f'Click the following link to reset your password:\n\n{reset_url}\n\nThis link will expire in 24 hours.',
                    settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@ecommerce.com',
                    [user.email],
                    fail_silently=False,
                )
                
                messages.success(request, 'Password reset link sent to your email.')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'No account found with this email address.')
    else:
        form = PasswordResetForm()
    
    return render(request, 'ecommerce/password_reset.html', {'form': form})


def password_reset_confirm(request, token):
    """Confirm password reset"""
    try:
        token_obj = PasswordResetToken.objects.get(token=token)
        
        if not token_obj.is_valid():
            messages.error(request, 'This reset link has expired or has already been used.')
            return redirect('password_reset_request')
        
        if request.method == 'POST':
            form = PasswordResetConfirmForm(request.POST)
            if form.is_valid():
                user = token_obj.user
                user.set_password(form.cleaned_data['password1'])
                user.save()
                
                token_obj.used = True
                token_obj.save()
                
                messages.success(request, 'Password reset successfully! Please log in.')
                return redirect('login')
        else:
            form = PasswordResetConfirmForm()
        
        return render(request, 'ecommerce/password_reset_confirm.html', {'form': form, 'token': token})
    
    except PasswordResetToken.DoesNotExist:
        messages.error(request, 'Invalid reset link.')
        return redirect('password_reset_request')

