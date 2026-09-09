from django.contrib import admin
from django.utils.html import format_html
from apps.orders.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'product_sku', 'selected_size', 'price', 'quantity', 'subtotal')
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'full_name', 'phone', 'city', 'state', 'formatted_grand_total', 'payment_status_badge', 'order_status_badge', 'created_at')
    list_filter = ('order_status', 'payment_status', 'payment_method', 'state', 'created_at')
    search_fields = ('order_number', 'full_name', 'email', 'phone', 'pincode', 'tracking_number')
    readonly_fields = ('order_number', 'created_at', 'updated_at', 'subtotal', 'tax_gst', 'grand_total')
    inlines = [OrderItemInline]

    fieldsets = (
        ('Order Identifiers', {
            'fields': ('order_number', 'user', 'created_at', 'updated_at')
        }),
        ('Customer & Delivery Contact', {
            'fields': ('full_name', 'email', 'phone')
        }),
        ('Sovereign Vault Delivery Address', {
            'fields': ('address_line1', 'address_line2', 'landmark', 'city', 'state', 'pincode')
        }),
        ('Status & Secure Logistics', {
            'fields': ('order_status', 'payment_status', 'payment_method', 'tracking_number')
        }),
        ('Financial Valuation (INR)', {
            'fields': ('subtotal', 'coupon_code', 'discount', 'tax_gst', 'grand_total')
        }),
        ('Complimentary Notes & Instructions', {
            'fields': ('gift_message', 'special_instructions')
        }),
    )

    def payment_status_badge(self, obj):
        color = '#28a745' if obj.payment_status == 'Paid' else '#ffc107' if obj.payment_status == 'Pending' else '#dc3545'
        return format_html('<span style="background-color: {}; color: #000; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 11px;">{}</span>', color, obj.payment_status)
    payment_status_badge.short_description = 'Payment'

    def order_status_badge(self, obj):
        colors = {
            'Confirmed': '#17a2b8',
            'Processing': '#6f42c1',
            'Dispatched': '#007bff',
            'Out for Delivery': '#fd7e14',
            'Delivered': '#28a745',
            'Cancelled': '#dc3545',
        }
        c = colors.get(obj.order_status, '#6c757d')
        return format_html('<span style="background-color: {}; color: #fff; padding: 3px 8px; border-radius: 4px; font-weight: 500; font-size: 11px;">{}</span>', c, obj.order_status)
    order_status_badge.short_description = 'Order Status'
