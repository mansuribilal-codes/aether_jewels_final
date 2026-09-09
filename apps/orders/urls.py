from django.urls import path
from apps.orders import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('success/<str:order_number>/', views.order_success_view, name='order_success'),
    path('detail/<str:order_number>/', views.order_detail_view, name='order_detail'),
    path('history/', views.order_history_view, name='order_history'),
    path('invoice/<str:order_number>/', views.order_invoice_view, name='order_invoice'),
]
