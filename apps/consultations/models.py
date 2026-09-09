from django.db import models


class ConsultationBooking(models.Model):
    CONSULTATION_TYPES = [
        ('Virtual VIP', 'Virtual High-Definition VIP Video Consultation'),
        ('Mumbai Flagship', 'Mumbai Flagship Atelier (Bandra West)'),
        ('Delhi Boutique', 'Delhi DLF Emporio Luxury Salon'),
        ('Bengaluru Lounge', 'Bengaluru UB City Private Suite'),
        ('Jaipur Heritage', 'Jaipur Sovereign Heritage Salon'),
    ]

    TIME_SLOTS = [
        ('11:00 AM - 01:00 PM', 'Morning Salon (11:00 AM - 01:00 PM)'),
        ('02:00 PM - 04:00 PM', 'Afternoon Soirée (02:00 PM - 04:00 PM)'),
        ('04:30 PM - 06:30 PM', 'Sunset Viewing (04:30 PM - 06:30 PM)'),
        ('07:00 PM - 09:00 PM', 'Private Evening Suite (07:00 PM - 09:00 PM)'),
    ]

    INTEREST_CATEGORIES = [
        ('Solitaires', 'Celestial High Solitaires & Engagement'),
        ('Bridal', 'Royal Bridal Sets & Astral Necklaces'),
        ('Bespoke', 'Bespoke Haute Joaillerie Commission'),
        ('Talismans', 'Zodiac & Planetary Talismans'),
        ('Everyday Fine', 'Minimalist Starlight & Solar Everyday Luxury'),
    ]

    BUDGET_RANGES = [
        ('₹1,00,000 - ₹3,00,000', '₹1,00,000 - ₹3,00,000'),
        ('₹3,00,000 - ₹7,50,000', '₹3,00,000 - ₹7,50,000'),
        ('₹7,50,000 - ₹15,00,000', '₹7,50,000 - ₹15,00,000'),
        ('₹15,00,000+ Sovereign', '₹15,00,000+ Sovereign Haute Joaillerie'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending Concierge Confirmation'),
        ('Confirmed', 'Confirmed with Personal Gemologist'),
        ('Completed', 'Consultation Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20, help_text="+91 98765 43210")
    consultation_type = models.CharField(max_length=50, choices=CONSULTATION_TYPES, default='Virtual VIP')
    preferred_date = models.DateField()
    time_slot = models.CharField(max_length=60, choices=TIME_SLOTS, default='02:00 PM - 04:00 PM')
    interest_category = models.CharField(max_length=50, choices=INTEREST_CATEGORIES, default='Solitaires')
    budget_range = models.CharField(max_length=50, choices=BUDGET_RANGES, default='₹3,00,000 - ₹7,50,000')
    notes = models.TextField(blank=True, help_text="Specific requirements, ring sizes, or gemstone preferences")
    
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "VIP Consultation Booking"
        verbose_name_plural = "VIP Consultation Bookings"

    def __str__(self):
        return f"{self.name} - {self.consultation_type} ({self.preferred_date})"


class BespokeInquiry(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=100, default="Mumbai")
    piece_type = models.CharField(max_length=100, default="Solitaire Ring", blank=True)
    metal_preference = models.CharField(max_length=100, default="18K Yellow / White Gold")
    gemstone_preference = models.CharField(max_length=100, default="Certified Natural Diamonds")
    carat_weight = models.DecimalField(max_digits=5, decimal_places=2, default=4.50, null=True, blank=True)
    setting_style = models.CharField(max_length=100, default="Astral Halo", blank=True)
    budget_estimate = models.CharField(max_length=100, default="₹3,00,000+")
    estimated_price_inr = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    custom_engraving = models.CharField(max_length=100, blank=True)
    design_idea = models.TextField(blank=True, help_text="Describe your dream piece or celestial concept")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Bespoke Design Commission"
        verbose_name_plural = "Bespoke Design Commissions"

    def __str__(self):
        return f"Bespoke: {self.name} ({self.piece_type} - {self.city})"

