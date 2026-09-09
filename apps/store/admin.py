from django.contrib import admin
from django.utils.html import format_html
from apps.store.models import Category, Product, ProductReview


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_featured', 'order', 'preview_image')
    list_editable = ('is_featured', 'order')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')

    def preview_image(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />', obj.image_url)
        return "-"
    preview_image.short_description = 'Thumbnail'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('preview_thumbnail', 'name', 'sku', 'category', 'formatted_price', 'metal_karat', 'gemstone_type', 'stock', 'is_featured', 'is_bestseller', 'is_available')
    list_editable = ('stock', 'is_featured', 'is_bestseller', 'is_available')
    list_filter = ('category', 'metal_karat', 'gemstone_type', 'is_available', 'is_featured', 'is_bestseller', 'is_new_arrival')
    search_fields = ('name', 'sku', 'tagline', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Master Identity', {
            'fields': ('category', 'name', 'slug', 'sku', 'tagline', 'price', 'original_price', 'stock', 'is_available')
        }),
        ('Curated Badges', {
            'fields': ('is_featured', 'is_bestseller', 'is_new_arrival')
        }),
        ('Craftsmanship & Gemological Specs', {
            'fields': ('metal_karat', 'metal_weight_grams', 'gemstone_type', 'diamond_carat', 'diamond_clarity', 'diamond_cut', 'certification', 'dimensions', 'size_options')
        }),
        ('Imagery', {
            'fields': ('image_url', 'image_url_2', 'image_url_3', 'image_url_4')
        }),
        ('Narrative & Copy', {
            'fields': ('short_description', 'description')
        }),
        ('Social Proof & Metrics', {
            'fields': ('rating', 'reviews_count', 'created_at', 'updated_at')
        }),
    )

    def preview_thumbnail(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" style="width: 55px; height: 55px; object-fit: cover; border-radius: 4px; border: 1px solid #d4af37;" />', obj.image_url)
        return "-"
    preview_thumbnail.short_description = 'Piece'


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'title', 'verified_purchase', 'created_at')
    list_filter = ('rating', 'verified_purchase', 'created_at')
    search_fields = ('product__name', 'user__username', 'title', 'comment')
