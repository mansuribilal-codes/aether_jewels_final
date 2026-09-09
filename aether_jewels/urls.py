"""
Root URL Configuration for Aether Jewels Haute Joaillerie platform.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Custom Admin Site Branding
admin.site.site_header = "Aether Jewels | Sovereign Haute Joaillerie"
admin.site.site_title = "Aether Jewels Admin"
admin.site.index_title = "Atelier Management & Sovereign Orders Portal"

from apps.store import views as store_views
from apps.consultations import views as consultation_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.store.urls', namespace='store')),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('cart/', include('apps.cart.urls', namespace='cart')),
    path('orders/', include('apps.orders.urls', namespace='orders')),
    path('consultations/', include('apps.consultations.urls', namespace='consultations')),
    path('developer/', store_views.developer_view, name='global_developer'),
    path('api/products/<int:product_id>/quickview/', store_views.api_product_quickview, name='api_quickview_global'),
    path('api/consultation/book/', consultation_views.api_book_consultation, name='api_book_global'),
    path('api/bespoke/inquire/', consultation_views.api_bespoke_inquiry, name='api_inquire_global'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
