from django.contrib import admin
from apps.consultations.models import ConsultationBooking, BespokeInquiry


@admin.register(ConsultationBooking)
class ConsultationBookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'consultation_type', 'preferred_date', 'time_slot', 'interest_category', 'budget_range', 'status', 'created_at')
    list_filter = ('consultation_type', 'status', 'interest_category', 'preferred_date')
    list_editable = ('status',)
    search_fields = ('name', 'email', 'phone', 'notes')


@admin.register(BespokeInquiry)
class BespokeInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'city', 'metal_preference', 'gemstone_preference', 'budget_estimate', 'created_at')
    list_filter = ('city', 'metal_preference', 'created_at')
    search_fields = ('name', 'email', 'phone', 'city', 'design_idea')
