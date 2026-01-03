def cart_count(request):
    """Context processor to add cart count to all templates"""
    cart_count = 0
    if request.user.is_authenticated and hasattr(request.user, 'role') and request.user.role == 'buyer':
        cart = request.session.get('cart', {})
        cart_count = sum(cart.values())
    return {'cart_count': cart_count}

