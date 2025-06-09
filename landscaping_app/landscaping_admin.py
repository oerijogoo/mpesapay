from django.contrib.admin import AdminSite
from .models import *
from .admin import (
    SiteSettingAdmin, ServiceAdmin, ProjectAdmin,
    TestimonialAdmin, TeamMemberAdmin, ContactMessageAdmin, HeroImageAdmin
)

class LandscapingAdminSite(AdminSite):
    site_header = "Landscaping Admin"
    site_title = "Landscaping Admin Portal"
    index_title = "Welcome to Landscaping Administration"

landscaping_admin_site = LandscapingAdminSite(name='landscaping_admin')

# Register only landscaping_app models
landscaping_admin_site.register(SiteSetting, SiteSettingAdmin)
landscaping_admin_site.register(Service, ServiceAdmin)
landscaping_admin_site.register(Project, ProjectAdmin)
landscaping_admin_site.register(Testimonial, TestimonialAdmin)
landscaping_admin_site.register(TeamMember, TeamMemberAdmin)
landscaping_admin_site.register(ContactMessage, ContactMessageAdmin)
landscaping_admin_site.register(HeroImage, HeroImageAdmin)
