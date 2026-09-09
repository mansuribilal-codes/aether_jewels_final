from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q

from apps.accounts.models import UserProfile
from apps.store.models import Category, Product, ProductReview
from apps.store.forms import ProductReviewForm, ContactForm


def home(request):
    featured_categories = Category.objects.filter(is_featured=True).order_by('order')[:6]
    bestsellers = Product.objects.filter(is_available=True, is_bestseller=True)[:6]
    featured_products = Product.objects.filter(is_available=True, is_featured=True)[:6]
    new_arrivals = Product.objects.filter(is_available=True, is_new_arrival=True)[:6]
    solitaires = Product.objects.filter(is_available=True, category__slug='high-solitaires')[:4]
    
    return render(request, 'store/home.html', {
        'featured_categories': featured_categories,
        'bestsellers': bestsellers,
        'featured_products': featured_products,
        'new_arrivals': new_arrivals,
        'solitaires': solitaires,
        'title': 'Celestial Haute Joaillerie & Fine Diamonds',
    })


def product_list(request):
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.all().order_by('order', 'name')
    
    # Search Query
    query = request.GET.get('q', '').strip()
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(tagline__icontains=query) |
            Q(description__icontains=query) |
            Q(sku__icontains=query) |
            Q(gemstone_type__icontains=query) |
            Q(metal_karat__icontains=query) |
            Q(category__name__icontains=query)
        )

    # Category Filter
    selected_category_slug = request.GET.get('category', '')
    selected_category = None
    if selected_category_slug:
        selected_category = get_object_or_404(Category, slug=selected_category_slug)
        products = products.filter(category=selected_category)

    # Price Filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass

    # Metal Filter
    metal = request.GET.get('metal', '')
    if metal:
        products = products.filter(metal_karat__icontains=metal)

    # Gemstone Filter
    gemstone = request.GET.get('gemstone', '')
    if gemstone:
        products = products.filter(gemstone_type__icontains=gemstone)

    # Sorting
    sort = request.GET.get('sort', 'featured')
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'newest':
        products = products.order_by('-created_at')
    elif sort == 'rating':
        products = products.order_by('-rating')
    elif sort == 'popular':
        products = products.order_by('-reviews_count')
    else:  # featured default
        products = products.order_by('-is_featured', '-created_at')

    # Available Metals & Gemstones for filter sidebar
    available_metals = Product.METAL_CHOICES
    available_gemstones = Product.GEMSTONE_CHOICES

    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'query': query,
        'min_price': min_price,
        'max_price': max_price,
        'selected_metal': metal,
        'selected_gemstone': gemstone,
        'selected_sort': sort,
        'available_metals': available_metals,
        'available_gemstones': available_gemstones,
        'total_count': products.count(),
        'title': f"{selected_category.name if selected_category else 'All High Jewellery'} | Aether Catalog",
    })


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    return product_list(request)  # Delegate to product_list with category set in GET or render seamlessly


def product_detail(request, category_slug, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    reviews = product.reviews.all()
    related_products = Product.objects.filter(category=product.category, is_available=True).exclude(id=product.id)[:4]
    
    review_form = ProductReviewForm()
    
    return render(request, 'store/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'related_products': related_products,
        'review_form': review_form,
        'title': f"{product.name} | Aether Jewels",
    })


@login_required
def submit_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()

            # Recalculate average rating
            all_reviews = product.reviews.all()
            if all_reviews.exists():
                avg = sum(r.rating for r in all_reviews) / len(all_reviews)
                product.rating = round(avg, 2)
                product.reviews_count = len(all_reviews)
                product.save()

            messages.success(request, "Your valuation review has been posted successfully.")
        else:
            messages.error(request, "Error submitting review. Please check all fields.")
    return redirect(product.get_absolute_url())


def developer_view(request):
    return render(request, 'pages/developer.html', {
        'title': 'Mohammed Bilal Mansuri | Full Stack Python Django Developer',
    })


def api_product_quickview(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return JsonResponse({
        'success': True,
        'product': {
            'id': product.id,
            'title': product.name,
            'subtitle': product.tagline or f"{product.metal_karat} • {product.gemstone_type}",
            'description': product.short_description or product.description[:200],
            'image_primary': product.image_url,
            'images': product.images_list,
            'price_inr': float(product.price),
            'formatted_price': product.formatted_price,
            'original_price': product.formatted_original_price,
            'discount_percent': product.discount_percent,
            'certification': product.certification,
            'primary_gemstone': product.gemstone_type,
            'metal_description': product.metal_karat,
            'carat_weight': float(product.diamond_carat) if product.diamond_carat else float(product.metal_weight_grams),
            'clarity': product.diamond_clarity,
            'cut': product.diamond_cut,
            'stock': product.stock,
            'sizes': product.sizes_list,
            'url': product.get_absolute_url(),
        }
    })


def about_view(request):
    return render(request, 'pages/about.html', {
        'title': 'Celestial Legacy & Craftsmanship | Aether Jewels'
    })


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, "Thank you for contacting Aether Jewels Concierge. A Senior Jewellery Specialist will reach out to you shortly.")
            return redirect('store:contact')
    else:
        form = ContactForm()

    return render(request, 'pages/contact.html', {
        'form': form,
        'title': 'VIP Concierge & Salons | Aether Jewels'
    })


def faq_view(request):
    return render(request, 'pages/faq.html', {
        'title': 'Hallmarking, Certification & Secure Transit FAQ'
    })

