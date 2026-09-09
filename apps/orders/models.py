from django.db import models
from django.contrib.auth.models import User
from apps.store.models import Product
import uuid


class Order(models.Model):
    STATUS_CHOICES = [
        ('Confirmed', 'Order Placed & Confirmed'),
        ('Processing', 'Crafting & Gemological Inspection'),
        ('Dispatched', 'Dispatched via Insured High-Value Armored Courier'),
        ('Out for Delivery', 'Out for White-Glove Delivery'),
        ('Delivered', 'Delivered to Customer'),
        ('Cancelled', 'Cancelled'),
    ]

    PAYMENT_METHODS = [
        ('UPI', 'Instant UPI / QR / Google Pay / PhonePe'),
        ('Card', 'Luxury Black / Metal / Credit & Debit Card'),
        ('NetBanking', 'Priority Net Banking (HDFC, ICICI, SBI, Axis)'),
        ('Vault_COD', 'VIP Insured Cash on Delivery (Assisted Inspection)'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('Paid', 'Paid & Verified'),
        ('Pending', 'Payment Pending / On Delivery'),
        ('Failed', 'Payment Failed'),
    ]

    order_number = models.CharField(max_length=40, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    
    # Customer Details
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    # Shipping Address
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    landmark = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    
    # Order Specifics
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHODS, default='UPI')
    payment_status = models.CharField(max_length=30, choices=PAYMENT_STATUS_CHOICES, default='Paid')
    order_status = models.CharField(max_length=40, choices=STATUS_CHOICES, default='Confirmed')
    
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_gst = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="3% Fine Jewellery GST")
    grand_total = models.DecimalField(max_digits=12, decimal_places=2)
    
    coupon_code = models.CharField(max_length=40, blank=True)
    gift_message = models.TextField(blank=True, help_text="Complimentary Celestial Hand-Written Calligraphy Note")
    special_instructions = models.TextField(blank=True)
    tracking_number = models.CharField(max_length=60, blank=True, default="AJ-SECURE-EXP-77291")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Luxury Order"
        verbose_name_plural = "Luxury Orders"

    def save(self, *args, **kwargs):
        if not self.order_number:
            uid = uuid.uuid4().hex[:8].upper()
            self.order_number = f"AJ-2026-{uid}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.order_number} - {self.full_name} (₹{self.grand_total})"

    @property
    def formatted_grand_total(self):
        val = int(self.grand_total)
        s = str(val)
        if len(s) <= 3:
            return f"₹{s}"
        last_three = s[-3:]
        remaining = s[:-3]
        out = ""
        while len(remaining) > 2:
            out = "," + remaining[-2:] + out
            remaining = remaining[:-2]
        if remaining:
            out = remaining + out
        return f"₹{out},{last_three}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=250)
    product_sku = models.CharField(max_length=60)
    product_image_url = models.CharField(max_length=500, blank=True)
    selected_size = models.CharField(max_length=20, default="Standard")
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.product_name} in #{self.order.order_number}"

    @property
    def subtotal(self):
        return self.price * self.quantity
