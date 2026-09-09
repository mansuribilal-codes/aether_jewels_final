from apps.cart.models import Cart, CartItem, Wishlist


def get_cart(request):
    """Retrieves or creates active shopping cart for authenticated user or anonymous session"""
    if request.user.is_authenticated:
        # Check if guest session cart exists and merge
        session_key = request.session.session_key
        if session_key:
            guest_carts = Cart.objects.filter(session_key=session_key, user__isnull=True)
            if guest_carts.exists():
                guest_cart = guest_carts.first()
                user_cart, _ = Cart.objects.get_or_create(user=request.user)
                
                # Merge items
                for g_item in guest_cart.items.all():
                    existing_item = user_cart.items.filter(product=g_item.product, selected_size=g_item.selected_size).first()
                    if existing_item:
                        existing_item.quantity += g_item.quantity
                        existing_item.save()
                    else:
                        g_item.cart = user_cart
                        g_item.save()
                
                if guest_cart.coupon_code and not user_cart.coupon_code:
                    user_cart.coupon_code = guest_cart.coupon_code
                    user_cart.save()
                
                guest_cart.delete()
                return user_cart

        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart
    else:
        if not request.session.session_key:
            request.session.save()
        session_key = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_key=session_key, user=None)
        return cart


def get_wishlist_product_ids(request):
    """Returns set of product IDs in the current user's wishlist"""
    if request.user.is_authenticated:
        return set(Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True))
    return set()
