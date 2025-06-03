from django.contrib import admin
from .models import (
    SiteSetting,
    ServiceCategory,
    Service,
    ServiceImage,
    Testimonial,
    ContactMessage,
    FAQ
)
from django.utils.html import format_html


class ServiceImageInline(admin.TabularInline):
    model = ServiceImage
    extra = 1
    readonly_fields = ['preview_image']

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="auto" />', obj.image.url)
        return "-"

    preview_image.short_description = 'Preview'


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'is_featured', 'created_at')
    list_filter = ('category', 'is_featured')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ServiceImageInline]

    fieldsets = (
        (None, {
            'fields': ('category', 'title', 'slug', 'featured_image')
        }),
        ('Details', {
            'fields': ('short_description', 'description', 'price')
        }),
        ('Settings', {
            'fields': ('is_featured',)
        }),
    )


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'phone', 'email')
    fieldsets = (
        ('Basic Info', {
            'fields': ('site_name', 'logo', 'favicon', 'motto')
        }),
        ('Contact Info', {
            'fields': ('phone', 'email', 'address')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'linkedin_url')
        }),
        ('About Us', {
            'fields': ('about_us',)
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description')
        }),
    )

    def has_add_permission(self, request):
        # Allow only one site setting
        count = SiteSetting.objects.all().count()
        if count == 0:
            return True
        return False


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_title', 'rating', 'is_active', 'created_at')
    list_filter = ('is_active', 'rating')
    search_fields = ('client_name', 'content')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read',)
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'phone', 'subject', 'message', 'created_at')

    def has_add_permission(self, request):
        return False


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('question', 'answer')