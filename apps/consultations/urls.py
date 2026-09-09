from django.urls import path
from apps.consultations import views

app_name = 'consultations'

urlpatterns = [
    path('book/', views.book_consultation_view, name='book'),
    path('bespoke/', views.bespoke_inquiry_view, name='bespoke'),
    path('success/<str:booking_type>/<int:item_id>/', views.consultation_success_view, name='success'),
    # AJAX API Endpoints
    path('api/book/', views.api_book_consultation, name='api_book'),
    path('api/inquire/', views.api_bespoke_inquiry, name='api_inquire'),
]

