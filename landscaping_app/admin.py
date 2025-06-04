# landscaping_app/admin.py

from django.contrib import admin
from django.utils.html import format_html

from .models import *

@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'phone', 'email')
    def has_add_permission(self, request):
        # Allow only one instance
        return not SiteSetting.objects.exists()

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_order')
    list_editable = ('display_order',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'service', 'date_completed', 'display_on_homepage')
    list_filter = ('service', 'display_on_homepage')
    search_fields = ('title', 'description')
    list_editable = ('display_on_homepage',)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'rating', 'display_on_homepage', 'created_at')
    list_editable = ('display_on_homepage',)
    list_filter = ('rating', 'display_on_homepage')

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'display_order')
    list_editable = ('display_order',)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read',)
    search_fields = ('name', 'email', 'subject')
    list_editable = ('is_read',)
    readonly_fields = ('created_at',)


@admin.register(HeroImage)
class HeroImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'display_order', 'image_preview')
    list_editable = ('is_active', 'display_order')
    list_filter = ('is_active',)
    search_fields = ('title', 'caption')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.image.url)
        return "-"

    image_preview.short_description = 'Preview'