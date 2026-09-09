from apps.cart.utils import get_cart, get_wishlist_product_ids
from apps.cart.models import Wishlist


def cart_context(request):
    """Context processor exposing cart item count, subtotal, and wishlist count"""
    try:
        cart = get_cart(request)
        cart_count = cart.total_items
        cart_subtotal = cart.subtotal
    except Exception:
        cart = None
        cart_count = 0
        cart_subtotal = 0

    wishlist_count = 0
    wishlist_ids = set()
    if request.user.is_authenticated:
        try:
            wishlist_count = Wishlist.objects.filter(user=request.user).count()
            wishlist_ids = get_wishlist_product_ids(request)
        except Exception:
            wishlist_count = 0

    return {
        'active_cart': cart,
        'cart_total_items': cart_count,
        'cart_subtotal': cart_subtotal,
        'wishlist_total_items': wishlist_count,
        'user_wishlist_ids': wishlist_ids,
    }
