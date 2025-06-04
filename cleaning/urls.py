from django.urls import path
from .views import (
    HomeView, ServiceListView, ServiceDetailView,
    GalleryView, AboutView, ContactView
)

app_name = 'cleaning'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('services/', ServiceListView.as_view(), name='services'),
    path('services/<slug:category_slug>/', ServiceListView.as_view(), name='services_by_category'),
    path('service/<slug:service_slug>/', ServiceDetailView.as_view(), name='service_detail'),
    path('gallery/', GalleryView.as_view(), name='gallery'),
    path('gallery/<slug:service_slug>/', GalleryView.as_view(), name='gallery_by_service'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
]