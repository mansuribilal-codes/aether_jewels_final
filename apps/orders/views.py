from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from apps.cart.utils import get_cart
from apps.orders.models import Order, OrderItem
from apps.orders.forms import CheckoutForm
import uuid


@login_required
def checkout_view(request):
    cart = get_cart(request)
    cart_items = cart.items.select_related('product').all()

    if not cart_items.exists():
        messages.warning(request, "Your shopping bag is empty. Please select a fine jewellery piece first.")
        return redirect('store:product_list')

    user = request.user
    profile = user.profile

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Create Order
                    order = form.save(commit=False)
                    order.user = user
                    order.subtotal = cart.subtotal
                    order.discount = cart.discount
                    order.tax_gst = cart.tax_gst
                    order.grand_total = cart.grand_total
                    order.coupon_code = cart.coupon_code or ''
                    
                    # Generate unique secure tracking number
                    order.tracking_number = f"AJ-SECURE-{uuid.uuid4().hex[:6].upper()}"
                    
                    # Payment Simulation
                    if order.payment_method == 'Vault_COD':
                        order.payment_status = 'Pending'
                    else:
                        order.payment_status = 'Paid'

                    order.save()

                    # Create OrderItems & update stock
                    for item in cart_items:
                        OrderItem.objects.create(
                            order=order,
                            product=item.product,
                            product_name=item.product.name,
                            product_sku=item.product.sku,
                            product_image_url=item.product.image_url,
                            selected_size=item.selected_size,
                            price=item.product.price,
                            quantity=item.quantity
                        )
                        # Decrement stock
                        if item.product.stock >= item.quantity:
                            item.product.stock -= item.quantity
                            item.product.save()

                    # Save address to profile if profile address is empty
                    if not profile.address_line1:
                        profile.phone_number = form.cleaned_data.get('phone', '')
                        profile.address_line1 = form.cleaned_data.get('address_line1', '')
                        profile.address_line2 = form.cleaned_data.get('address_line2', '')
                        profile.landmark = form.cleaned_data.get('landmark', '')
                        profile.city = form.cleaned_data.get('city', '')
                        profile.state = form.cleaned_data.get('state', '')
                        profile.pincode = form.cleaned_data.get('pincode', '')
                        profile.save()

                    # Clear Cart
                    cart.items.all().delete()
                    cart.coupon_code = ''
                    cart.save()

                messages.success(request, f"✨ Sovereign Order #{order.order_number} confirmed with White-Glove Insured Delivery.")
                return redirect('orders:order_success', order_number=order.order_number)

            except Exception as e:
                messages.error(request, f"An error occurred while securing your order: {str(e)}")
        else:
            messages.error(request, "Please review the checkout form fields and ensure valid 10-digit phone and 6-digit Indian PIN code.")
    else:
        # Pre-populate form with user profile
        initial_data = {
            'full_name': f"{user.first_name} {user.last_name}".strip() or user.username,
            'email': user.email,
            'phone': profile.phone_number,
            'address_line1': profile.address_line1,
            'address_line2': profile.address_line2,
            'landmark': profile.landmark,
            'city': profile.city or 'Ahmedabad',
            'state': profile.state or 'Gujarat',
            'pincode': profile.pincode or '380001',
            'payment_method': 'UPI',
        }
        form = CheckoutForm(initial=initial_data)

    return render(request, 'orders/checkout.html', {
        'form': form,
        'cart': cart,
        'cart_items': cart_items,
        'title': 'Secure Sovereign Checkout | Aether Jewels',
    })


@login_required
def order_success_view(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'orders/order_success.html', {
        'order': order,
        'title': f'Order Confirmed #{order.order_number} | Aether Jewels',
    })


@login_required
def order_detail_view(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'orders/order_detail.html', {
        'order': order,
        'title': f'Order #{order.order_number} Details',
    })


@login_required
def order_history_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {
        'orders': orders,
        'title': 'Order History & Vault Records',
    })


@login_required
def order_invoice_view(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'orders/order_invoice.html', {
        'order': order,
        'title': f'Tax Invoice #{order.order_number} - Aether Jewels',
    })
