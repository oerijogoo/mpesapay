# landscaping_app/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages


def get_site_settings():
    return SiteSetting.objects.first()


def index(request):
    context = {
        'site_settings': get_site_settings(),
        'services': Service.objects.all()[:6],
        'featured_projects': Project.objects.filter(display_on_homepage=True)[:4],
        'testimonials': Testimonial.objects.filter(display_on_homepage=True),
    }
    return render(request, 'landscaping_app/index.html', context)


def services(request):
    context = {
        'site_settings': get_site_settings(),
        'services': Service.objects.all(),
    }
    return render(request, 'landscaping_app/services.html', context)


def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    related_projects = Project.objects.filter(service=service)[:4]

    context = {
        'site_settings': get_site_settings(),
        'service': service,
        'related_projects': related_projects,
    }
    return render(request, 'landscaping_app/service_detail.html', context)


def gallery(request):
    context = {
        'site_settings': get_site_settings(),
        'projects': Project.objects.all().order_by('-date_completed'),
    }
    return render(request, 'landscaping_app/gallery.html', context)


def about(request):
    context = {
        'site_settings': get_site_settings(),
        'team_members': TeamMember.objects.all(),
    }
    return render(request, 'landscaping_app/about.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            message = form.save()

            # Send email notification
            send_mail(
                f"New Contact Message: {message.subject}",
                f"You have received a new message from {message.name} ({message.email}):\n\n{message.message}",
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],
                fail_silently=False,
            )

            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')
    else:
        form = ContactForm()

    context = {
        'site_settings': get_site_settings(),
        'form': form,
    }
    return render(request, 'landscaping_app/contact.html', context)