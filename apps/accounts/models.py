from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    VIP_TIERS = [
        ('Member', 'Aether Member'),
        ('Silver Astral', 'Silver Astral'),
        ('Gold Celestial', 'Gold Celestial'),
        ('Solitaire Platinum', 'Solitaire Platinum VIP'),
    ]

    INDIAN_STATES = [
        ('Andhra Pradesh', 'Andhra Pradesh'),
        ('Delhi', 'Delhi NCR'),
        ('Gujarat', 'Gujarat'),
        ('Karnataka', 'Karnataka'),
        ('Maharashtra', 'Maharashtra'),
        ('Rajasthan', 'Rajasthan'),
        ('Tamil Nadu', 'Tamil Nadu'),
        ('Telangana', 'Telangana'),
        ('Uttar Pradesh', 'Uttar Pradesh'),
        ('West Bengal', 'West Bengal'),
        ('Other', 'Other State/UT'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True, help_text="+91 98765 43210")
    alternate_phone = models.CharField(max_length=15, blank=True)
    address_line1 = models.CharField(max_length=255, blank=True, verbose_name="Address Line 1")
    address_line2 = models.CharField(max_length=255, blank=True, verbose_name="Address Line 2 (Apartment, Suite)")
    landmark = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True, default="Ahmedabad")
    state = models.CharField(max_length=100, blank=True, default="Gujarat", choices=INDIAN_STATES)
    pincode = models.CharField(max_length=10, blank=True, default="380001")
    vip_tier = models.CharField(max_length=30, choices=VIP_TIERS, default='Member')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.vip_tier})"

    @property
    def full_address(self):
        parts = [self.address_line1, self.address_line2, self.landmark, self.city, self.state, self.pincode]
        return ", ".join([p for p in parts if p])


@receiver(post_save, sender=User)
def create_or_save_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()
        else:
            UserProfile.objects.create(user=instance)
