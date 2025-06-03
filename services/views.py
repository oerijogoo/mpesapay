from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Service, ServiceCategory, Testimonial, FAQ, SiteSetting
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse


def home(request):
    featured_services = Service.objects.filter(is_featured=True)[:6]
    categories = ServiceCategory.objects.all()
    testimonials = Testimonial.objects.filter(is_active=True)[:5]

    context = {
        'featured_services': featured_services,
        'categories': categories,
        'testimonials': testimonials,
    }
    return render(request, 'home.html', context)


class ServiceListView(ListView):
    model = Service
    template_name = 'services/list.html'
    context_object_name = 'services'
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.kwargs.get('category_slug')

        if category_slug:
            category = get_object_or_404(ServiceCategory, slug=category_slug)
            queryset = queryset.filter(category=category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ServiceCategory.objects.all()
        context['selected_category'] = self.kwargs.get('category_slug')
        return context


class ServiceDetailView(DetailView):
    model = Service
    template_name = 'services/detail.html'
    context_object_name = 'service'
    slug_url_kwarg = 'service_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_services'] = Service.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:4]
        return context


def about(request):
    testimonials = Testimonial.objects.filter(is_active=True)
    faqs = FAQ.objects.filter(is_active=True)

    context = {
        'testimonials': testimonials,
        'faqs': faqs,
    }
    return render(request, 'about.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()

            # Send email notification
            if settings.DEFAULT_FROM_EMAIL:
                send_mail(
                    f"New Contact Message: {contact_message.subject}",
                    f"Name: {contact_message.name}\nEmail: {contact_message.email}\nPhone: {contact_message.phone}\n\nMessage:\n{contact_message.message}",
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.DEFAULT_FROM_EMAIL],
                    fail_silently=True,
                )

            messages.success(request, 'Thank you for your message. We will get back to you soon!')
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ContactForm()

    context = {
        'form': form,
    }
    return render(request, 'contact.html', context)