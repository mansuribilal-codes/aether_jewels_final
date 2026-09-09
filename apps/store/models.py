from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    image_url = models.CharField(max_length=600, blank=True)
    description = models.TextField(blank=True)
    is_featured = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Jewellery Category"
        verbose_name_plural = "Jewellery Categories"
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:category_detail', args=[self.slug])


class Product(models.Model):
    METAL_CHOICES = [
        ('18K Yellow Gold', '18K Yellow Gold'),
        ('18K Rose Gold', '18K Rose Gold'),
        ('18K White Gold', '18K White Gold'),
        ('22K Royal Gold', '22K Royal Gold'),
        ('950 Pure Platinum', '950 Pure Platinum'),
        ('Dual Tone 18K Gold', 'Dual Tone 18K Gold & Platinum'),
    ]

    GEMSTONE_CHOICES = [
        ('Natural Diamond', 'Solitaire & Natural Diamond'),
        ('Zambian Emerald', 'Royal Zambian Emerald'),
        ('Ceylon Sapphire', 'Kashmir/Ceylon Blue Sapphire'),
        ('Burmese Ruby', 'Pigeon Blood Burmese Ruby'),
        ('Tanzanite & Diamond', 'Celestial Tanzanite & Diamond'),
        ('South Sea Pearl', 'Lustrous South Sea Pearl'),
        ('Moissanite VVS', 'Celestial Moissanite & Diamond'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    sku = models.CharField(max_length=50, unique=True, help_text="e.g. AJ-RNG-01")
    tagline = models.CharField(max_length=255, blank=True, help_text="e.g. Celestial Constellation in 18K Gold")
    
    price = models.DecimalField(max_digits=12, decimal_places=2, help_text="Price in INR (₹)")
    original_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="Original MRP before discount in INR (₹)")
    stock = models.PositiveIntegerField(default=5)
    is_available = models.BooleanField(default=True)
    
    is_featured = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=False)

    short_description = models.TextField(help_text="Summary for cards and fast overview")
    description = models.TextField(help_text="Detailed craftsmanship narrative")

    # Jewellery Specifications
    metal_karat = models.CharField(max_length=60, choices=METAL_CHOICES, default='18K Yellow Gold')
    metal_weight_grams = models.DecimalField(max_digits=6, decimal_places=2, default=5.50, help_text="Gross weight in grams")
    gemstone_type = models.CharField(max_length=80, choices=GEMSTONE_CHOICES, default='Natural Diamond')
    diamond_carat = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Diamond total weight in carats")
    diamond_clarity = models.CharField(max_length=50, default="VVS1 - IF", blank=True)
    diamond_cut = models.CharField(max_length=50, default="Ideal Round Brilliant", blank=True)
    certification = models.CharField(max_length=150, default="100% BIS Hallmarked & IGI / SGL Certified")
    dimensions = models.CharField(max_length=100, blank=True, default="Standard Luxury Proportion")
    size_options = models.CharField(max_length=100, blank=True, default="6,7,8,9,10,12,14", help_text="Comma-separated ring/bangle sizes")

    # Imagery
    image_url = models.CharField(max_length=600, help_text="Primary High-Res Product Image URL")
    image_url_2 = models.CharField(max_length=600, blank=True, help_text="Angle 2 / Model view")
    image_url_3 = models.CharField(max_length=600, blank=True, help_text="Angle 3 / Macro gemstone view")
    image_url_4 = models.CharField(max_length=600, blank=True, help_text="Angle 4 / Luxury packaging view")

    rating = models.DecimalField(max_digits=3, decimal_places=2, default=4.9)
    reviews_count = models.PositiveIntegerField(default=18)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Fine Jewellery Piece"
        verbose_name_plural = "Fine Jewellery Pieces"
        ordering = ['-is_featured', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.sku})"

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.category.slug, self.slug])

    @property
    def discount_percent(self):
        if self.original_price and self.original_price > self.price:
            diff = self.original_price - self.price
            return int((diff / self.original_price) * 100)
        return 0

    @property
    def formatted_price(self):
        # Format in Indian Rupee format e.g. ₹ 1,25,000
        val = int(self.price)
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

    @property
    def formatted_original_price(self):
        if not self.original_price:
            return None
        val = int(self.original_price)
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

    @property
    def images_list(self):
        imgs = [self.image_url]
        if self.image_url_2: imgs.append(self.image_url_2)
        if self.image_url_3: imgs.append(self.image_url_3)
        if self.image_url_4: imgs.append(self.image_url_4)
        return imgs

    @property
    def sizes_list(self):
        if self.size_options:
            return [s.strip() for s in self.size_options.split(',') if s.strip()]
        return []


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')], default=5)
    title = models.CharField(max_length=150)
    comment = models.TextField()
    verified_purchase = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating}★)"
