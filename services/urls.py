from django.urls import path
from .views import (
    home,
    ServiceListView,
    ServiceDetailView,
    about,
    contact
)

urlpatterns = [
    path('', home, name='home'),
    path('services/', ServiceListView.as_view(), name='service_list'),
    path('services/<slug:category_slug>/', ServiceListView.as_view(), name='service_list_by_category'),
    path('services/detail/<slug:service_slug>/', ServiceDetailView.as_view(), name='service_detail'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
]