# admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import CustomUserModel, ServiceProvider, ServiceProviderUser

@admin.register(CustomUserModel)
class CustomUserModelAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'is_verified', 'is_active']
    list_filter = ['is_verified', 'is_active', 'role']
    search_fields = ['email', 'username']
    readonly_fields = ['user_id']

@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ['service_name', 'service_id', 'redirect_url']
    readonly_fields = ['service_id', 'decrypted_service_secret']
    fields = ['service_name', 'service_id', 'claims_required', 'redirect_url', 'decrypted_service_secret']
    
    def decrypted_service_secret(self, obj):
        """Display the decrypted service secret as read-only"""
        if obj and obj.service_secret:
            return format_html(
                '<code style="background-color: #f8f8f8; padding: 4px; border-radius: 4px; font-family: monospace;">{}</code>',
                obj.service_secret
            )
        return "No secret generated"
    
    decrypted_service_secret.short_description = "Service Secret (Decrypted)"
    decrypted_service_secret.help_text = "This is the decrypted service secret. Keep this secure!"

@admin.register(ServiceProviderUser)
class ServiceProviderUserAdmin(admin.ModelAdmin):
    list_display = ['serviceprovider', 'user', 'is_active', 'granted_at']
    list_filter = ['is_active', 'granted_at']
    readonly_fields = ['granted_at']