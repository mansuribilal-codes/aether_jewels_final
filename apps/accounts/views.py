from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.accounts.forms import UserRegisterForm, UserProfileEditForm
from apps.orders.models import Order
from apps.cart.models import Cart, Wishlist


def register_view(request):
    if request.user.is_authenticated:
        return redirect('store:home')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Update UserProfile
            profile = user.profile
            profile.phone_number = form.cleaned_data.get('phone_number', '')
            profile.city = form.cleaned_data.get('city', '')
            profile.state = form.cleaned_data.get('state', '')
            profile.save()

            session_key = request.session.session_key
            guest_cart = None
            if session_key:
                guest_cart = Cart.objects.filter(session_key=session_key, user__isnull=True).first()

            login(request, user)

            if guest_cart:
                user_cart, _ = Cart.objects.get_or_create(user=user)
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

            messages.success(request, f"Welcome to the Celestial Realm, {user.first_name or user.username}! Your Aether Membership is now active.")
            next_url = request.GET.get('next') or 'store:home'
            return redirect(next_url)
        else:
            messages.error(request, "Please review the registration form errors below.")
    else:
        form = UserRegisterForm()

    return render(request, 'accounts/register.html', {'form': form, 'title': 'Join Aether Privilege Club'})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('store:home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                # Retain guest cart before session cycling
                session_key = request.session.session_key
                guest_cart = None
                if session_key:
                    guest_cart = Cart.objects.filter(session_key=session_key, user__isnull=True).first()

                login(request, user)

                # Merge guest cart to user cart
                if guest_cart:
                    user_cart, _ = Cart.objects.get_or_create(user=user)
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

                messages.success(request, f"Welcome back, {user.first_name or user.username}.")
                next_url = request.GET.get('next') or request.POST.get('next') or 'store:home'
                return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password credentials.")
    else:
        form = AuthenticationForm()

    next_url = request.GET.get('next', '')
    return render(request, 'accounts/login.html', {'form': form, 'next': next_url, 'title': 'Sovereign Sign In'})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been safely signed out. We look forward to welcoming you again.")
    return redirect('store:home')


@login_required
def profile_view(request):
    user = request.user
    profile = user.profile
    orders = Order.objects.filter(user=user).order_by('-created_at')
    wishlist_items = Wishlist.objects.filter(user=user).select_related('product')
    
    total_spent = sum(o.grand_total for o in orders if o.payment_status == 'Paid')

    return render(request, 'accounts/profile.html', {
        'user': user,
        'profile': profile,
        'orders': orders,
        'wishlist_items': wishlist_items,
        'total_spent': total_spent,
        'title': 'VIP Sovereign Portal',
    })


@login_required
def edit_profile_view(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        form = UserProfileEditForm(request.POST, instance=profile)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            form.save()
            messages.success(request, "Your personal details and delivery vault address have been updated.")
            return redirect('accounts:profile')
        else:
            messages.error(request, "Please check the form for errors.")
    else:
        initial_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }
        form = UserProfileEditForm(instance=profile, initial=initial_data)

    return render(request, 'accounts/edit_profile.html', {
        'form': form,
        'title': 'Edit Profile & Vault Address',
    })
