from django.contrib import admin
from .models import SiteSetting, ServiceCategory, Service, GalleryImage, Testimonial, ContactMessage

class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'phone', 'email')
    def has_add_permission(self, request):
        # Allow only one site setting instance
        return not SiteSetting.objects.exists()

class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_featured', 'display_order')
    list_editable = ('is_featured', 'display_order')
    prepopulated_fields = {'slug': ('name',)}

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_featured', 'display_order')
    list_filter = ('category', 'is_featured')
    list_editable = ('is_featured', 'display_order', 'price')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('caption', 'service', 'is_featured', 'display_order')
    list_filter = ('service', 'is_featured')
    list_editable = ('is_featured', 'display_order')
    search_fields = ('caption',)

class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_title', 'rating', 'is_featured', 'display_order')
    list_editable = ('is_featured', 'display_order', 'rating')
    search_fields = ('client_name', 'content')

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    list_editable = ('is_read',)
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)

admin.site.register(SiteSetting, SiteSettingAdmin)
admin.site.register(ServiceCategory, ServiceCategoryAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(GalleryImage, GalleryImageAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)