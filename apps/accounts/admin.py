from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from apps.accounts.models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'VIP Profile & Vault Address'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_vip_tier', 'get_phone', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'profile__vip_tier', 'profile__state')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'profile__phone_number', 'profile__city')

    def get_vip_tier(self, obj):
        return obj.profile.vip_tier if hasattr(obj, 'profile') else '-'
    get_vip_tier.short_description = 'VIP Tier'

    def get_phone(self, obj):
        return obj.profile.phone_number if hasattr(obj, 'profile') else '-'
    get_phone.short_description = 'Phone (+91)'


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'vip_tier', 'phone_number', 'city', 'state', 'pincode', 'created_at')
    list_filter = ('vip_tier', 'state')
    search_fields = ('user__username', 'user__email', 'phone_number', 'city', 'pincode')
