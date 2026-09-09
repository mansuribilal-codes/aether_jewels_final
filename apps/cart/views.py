from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from apps.cart.utils import get_cart
from apps.cart.models import CartItem, Wishlist, Coupon
from apps.store.models import Product


def cart_detail(request):
    cart = get_cart(request)
    cart_items = cart.items.select_related('product').all()
    
    return render(request, 'cart/cart_detail.html', {
        'cart': cart,
        'cart_items': cart_items,
        'title': 'Your Celestial Bag | Aether Jewels',
    })


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_available=True)
    cart = get_cart(request)

    selected_size = request.POST.get('size', request.GET.get('size', 'Standard'))
    if not selected_size:
        selected_size = 'Standard'

    try:
        qty = int(request.POST.get('quantity', request.GET.get('quantity', 1)))
        qty = max(1, qty)
    except ValueError:
        qty = 1

    if product.stock < qty:
        messages.error(request, f"Apologies, only {product.stock} units available in our vault.")
        return redirect(product.get_absolute_url())

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        selected_size=selected_size,
        defaults={'quantity': qty}
    )

    if not created:
        if cart_item.quantity + qty <= product.stock:
            cart_item.quantity += qty
            cart_item.save()
        else:
            cart_item.quantity = product.stock
            cart_item.save()
            messages.warning(request, f"Item quantity adjusted to maximum available vault stock ({product.stock}).")

    messages.success(request, f"✨ {product.name} ({selected_size}) added to your shopping bag.")
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'cart_count': cart.total_items,
            'message': f"{product.name} added to cart."
        })

    next_url = request.POST.get('next') or request.GET.get('next') or 'cart:cart_detail'
    return redirect(next_url)


def update_cart_quantity(request, item_id):
    cart = get_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)

    action = request.POST.get('action')
    try:
        new_qty = int(request.POST.get('quantity', item.quantity))
    except ValueError:
        new_qty = item.quantity

    if action == 'increment':
        if item.quantity < item.product.stock:
            item.quantity += 1
            item.save()
            messages.success(request, f"Updated quantity for {item.product.name}.")
        else:
            messages.warning(request, f"Only {item.product.stock} units in vault stock.")
    elif action == 'decrement':
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
            messages.info(request, f"Decreased quantity for {item.product.name}.")
        else:
            item.delete()
            messages.info(request, f"Removed {item.product.name} from bag.")
    elif action == 'set':
        if new_qty > 0 and new_qty <= item.product.stock:
            item.quantity = new_qty
            item.save()
        elif new_qty > item.product.stock:
            item.quantity = item.product.stock
            item.save()
            messages.warning(request, f"Quantity capped at available stock ({item.product.stock}).")
        else:
            item.delete()

    return redirect('cart:cart_detail')


def remove_from_cart(request, item_id):
    cart = get_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    product_name = item.product.name
    item.delete()
    messages.info(request, f"Removed {product_name} from your shopping bag.")
    return redirect('cart:cart_detail')


def apply_coupon(request):
    if request.method == 'POST':
        code = request.POST.get('coupon_code', '').strip().upper()
        cart = get_cart(request)
        
        try:
            coupon = Coupon.objects.get(code__iexact=code, is_active=True)
            if cart.subtotal >= coupon.min_purchase:
                cart.coupon_code = coupon.code
                cart.save()
                messages.success(request, f"Privilege code '{coupon.code}' applied successfully!")
            else:
                messages.error(request, f"Code '{code}' requires a minimum order of ₹{int(coupon.min_purchase):,}.")
        except Coupon.DoesNotExist:
            messages.error(request, f"Invalid or expired privilege coupon code '{code}'.")

    return redirect('cart:cart_detail')


def remove_coupon(request):
    cart = get_cart(request)
    cart.coupon_code = ''
    cart.save()
    messages.info(request, "Privilege coupon removed.")
    return redirect('cart:cart_detail')


@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'cart/wishlist.html', {
        'wishlist_items': wishlist_items,
        'title': 'Your Sovereign Wishlist | Aether Jewels',
    })


def toggle_wishlist(request, product_id):
    if not request.user.is_authenticated:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'login_required', 'login_url': '/accounts/login/?next=' + request.path}, status=401)
        messages.info(request, "Please sign in to save pieces to your Sovereign Wishlist.")
        return redirect('accounts:login')

    product = get_object_or_404(Product, id=product_id)
    wishlist_item = Wishlist.objects.filter(user=request.user, product=product).first()

    if wishlist_item:
        wishlist_item.delete()
        action = 'removed'
        msg = f"{product.name} removed from your wishlist."
    else:
        Wishlist.objects.create(user=request.user, product=product)
        action = 'added'
        msg = f"✨ {product.name} added to your Sovereign Wishlist."

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        count = Wishlist.objects.filter(user=request.user).count()
        return JsonResponse({'status': 'success', 'action': action, 'message': msg, 'wishlist_count': count})

    messages.success(request, msg)
    next_url = request.META.get('HTTP_REFERER') or 'cart:wishlist'
    return redirect(next_url)


@login_required
def move_wishlist_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_available=True)
    cart = get_cart(request)

    # Add to cart
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        selected_size='Standard',
        defaults={'quantity': 1}
    )
    if not created and cart_item.quantity < product.stock:
        cart_item.quantity += 1
        cart_item.save()

    # Remove from wishlist
    Wishlist.objects.filter(user=request.user, product=product).delete()

    messages.success(request, f"✨ Moved {product.name} to your shopping bag.")
    return redirect('cart:cart_detail')
