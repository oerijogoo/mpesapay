"""
URL configuration for payments project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an iimport:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings 
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from landscaping_app.landscaping_admin import landscaping_admin_site
 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('mpesa/', include('mpesa_express.urls')),
    path('', include('store.urls')),
    path('cart/', include('cart.urls')),
    path('payment/', include('payment.urls')),
    path('savings/', include('savings.urls')),
    path('loans/', include('loans.urls')),
    path('shares/', include('shares.urls')),
    path('members/', include('members.urls')),
    # path('accounting/', include('accounting.urls')),
    path('reports/', include('reports.urls')),
    path('search/', include('search.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('hospital/', include('hospital.urls')),
    path('isms/', include('isms.urls')),
    path('clean/', include('cleaning.urls')),
    path('cleaning/', include('services.urls')),
    path('landscaping/', include('landscaping_app.urls')),
    path("landscaping-admin/", landscaping_admin_site.urls),
    # path('accounts/login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    # path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

