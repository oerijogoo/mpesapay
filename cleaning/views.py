from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import FormView
from .models import Service, ServiceCategory, GalleryImage, Testimonial, SiteSetting
from .forms import ContactForm
from django.urls import reverse_lazy
from django.contrib import messages

class HomeView(TemplateView):
    template_name = 'cleaning/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_categories'] = ServiceCategory.objects.filter(is_featured=True)
        context['featured_services'] = Service.objects.filter(is_featured=True)
        context['testimonials'] = Testimonial.objects.filter(is_featured=True)
        return context

class ServiceListView(ListView):
    model = Service
    template_name = 'cleaning/services.html'
    context_object_name = 'services'

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(ServiceCategory, slug=category_slug)
            return Service.objects.filter(category=category)
        return Service.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ServiceCategory.objects.all()
        context['selected_category'] = self.kwargs.get('category_slug')
        return context

class ServiceDetailView(DetailView):
    model = Service
    template_name = 'cleaning/service_detail.html'
    context_object_name = 'service'
    slug_url_kwarg = 'service_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_services'] = Service.objects.filter(category=self.object.category).exclude(id=self.object.id)[:3]
        return context

class GalleryView(ListView):
    model = GalleryImage
    template_name = 'cleaning/gallery.html'
    context_object_name = 'gallery_images'

    def get_queryset(self):
        service_slug = self.kwargs.get('service_slug')
        if service_slug:
            service = get_object_or_404(Service, slug=service_slug)
            return GalleryImage.objects.filter(service=service)
        return GalleryImage.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.all()
        context['selected_service'] = self.kwargs.get('service_slug')
        return context

class AboutView(TemplateView):
    template_name = 'cleaning/about.html'

class ContactView(FormView):
    template_name = 'cleaning/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Your message has been sent successfully. We will get back to you soon!')
        return super().form_valid(form)