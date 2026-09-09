from django.contrib import admin
from apps.cart.models import Cart, CartItem, Wishlist, Coupon


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    fields = ('product', 'selected_size', 'quantity', 'subtotal')
    readonly_fields = ('subtotal',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'coupon_code', 'total_items', 'subtotal', 'grand_total', 'created_at', 'updated_at')
    search_fields = ('user__username', 'session_key', 'coupon_code')
    inlines = [CartItemInline]


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'product__name')


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'description', 'discount_percent', 'discount_amount', 'min_purchase', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('code', 'description')
