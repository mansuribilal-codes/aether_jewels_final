from django.urls import path
from apps.store import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.product_list, name='product_list'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('product/<slug:category_slug>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/review/', views.submit_review, name='submit_review'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('faq/', views.faq_view, name='faq'),
    path('developer/', views.developer_view, name='developer'),
    path('api/products/<int:product_id>/quickview/', views.api_product_quickview, name='api_product_quickview'),
]

