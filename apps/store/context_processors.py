from apps.store.models import Category
import datetime


def store_context(request):
    """Global context processor for categories menu, site branding, and current year"""
    categories = Category.objects.all().order_by('order', 'name')
    return {
        'nav_categories': categories,
        'SITE_NAME': 'Aether Jewels',
        'SITE_TAGLINE': 'Celestial Haute Joaillerie',
        'CURRENT_YEAR': datetime.date.today().year,
        'SUPPORT_PHONE': '+91 800 238 4371',
        'CONCIERGE_EMAIL': 'concierge@aetherjewels.com',
    }
