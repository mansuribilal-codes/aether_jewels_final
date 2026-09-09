from django.db import models
from django.contrib.auth.models import User
from apps.store.models import Product
from decimal import Decimal


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='carts')
    session_key = models.CharField(max_length=60, null=True, blank=True, db_index=True)
    coupon_code = models.CharField(max_length=30, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user:
            return f"Cart of {self.user.username}"
        return f"Guest Cart ({self.session_key})"

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def subtotal(self):
        return sum(item.subtotal for item in self.items.all())

    @property
    def discount(self):
        if not self.coupon_code:
            return Decimal('0.00')
        try:
            coupon = Coupon.objects.get(code__iexact=self.coupon_code, is_active=True)
            if self.subtotal >= coupon.min_purchase:
                if coupon.discount_percent > 0:
                    return (self.subtotal * Decimal(coupon.discount_percent)) / Decimal(100)
                elif coupon.discount_amount > 0:
                    return min(coupon.discount_amount, self.subtotal)
        except Coupon.DoesNotExist:
            pass
        return Decimal('0.00')

    @property
    def tax_gst(self):
        # 3% GST standard on luxury fine jewellery in India
        taxable_amount = max(Decimal('0.00'), self.subtotal - self.discount)
        return (taxable_amount * Decimal('0.03')).quantize(Decimal('0.01'))

    @property
    def grand_total(self):
        taxable_amount = max(Decimal('0.00'), self.subtotal - self.discount)
        return taxable_amount + self.tax_gst


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    selected_size = models.CharField(max_length=20, default="Standard", blank=True)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('cart', 'product', 'selected_size')

    def __str__(self):
        return f"{self.quantity}x {self.product.name} (Size: {self.selected_size})"

    @property
    def subtotal(self):
        return self.product.price * self.quantity


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        verbose_name = "Wishlist Item"
        verbose_name_plural = "Wishlist Items"

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


class Coupon(models.Model):
    code = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=200, help_text="e.g. 10% Celestial Privilege Discount")
    discount_percent = models.PositiveIntegerField(default=0, help_text="e.g. 10 for 10%")
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Flat INR off e.g. 5000")
    min_purchase = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Minimum order value in INR")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} ({self.discount_percent}% / ₹{self.discount_amount} off)"
