from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, UpdateUserForm
from django.contrib.sites.shortcuts import get_current_site
from .token import user_tokenizer_generate
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.models import auth 
from django.contrib.auth import authenticate



def register(request):
    form = CreateUserForm()  # Initialize the form

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save yet, we need to modify it first
            user.is_active = False  # Set user as inactive
            user.save()

            # Email verification setup
            current_site = get_current_site(request)
            subject = "Account verification email"
            message = render_to_string('account/registration/email-verification.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user_tokenizer_generate.make_token(user),
            })

            user.email_user(subject=subject, message=message)
            messages.success(request, "Registration successful! Please check your email to verify your account.")
            return redirect('email-verification-sent')

    context = {'form': form}
    return render(request, 'account/registration/register.html', context)

def email_verification(request, uidb64, token):
    try:
        unique_id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=unique_id)

        if user_tokenizer_generate.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Your email has been verified successfully!")
            return redirect('email-verification-success')
        else:
            messages.error(request, "Email verification failed. Invalid token.")
            return redirect('email-verification-fail')

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, "Invalid verification link.")
        return redirect('email-verification-fail')

def email_verification_sent(request):
    return render(request, 'account/registration/email-verification-sent.html')

def email_verification_success(request):
    return render(request, 'account/registration/email-verification-success.html')

def email_verification_failed(request):
    return render(request, 'account/registration/email-verification-failed.html')


def my_login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)  # Pass the user object, not User class
                return redirect("dashboard")
            else:
                messages.error(request, "Invalid username or password.")

    context = {'form': form}
    return render(request, 'account/my-login.html', context=context)


def user_logout(request):
    auth.logout(request)

    return redirect("store")


def dashboard(request):
    return render(request, 'account/dashboard.html')


def profile_management(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Profile updated successfully!")  # Optional: Add a success message
            return redirect('dashboard')  # Redirect after successful update
    else:
        user_form = UpdateUserForm(instance=request.user)

    return render(request, 'account/profile-management.html', {'user_form': user_form})  # Use the same variable name

def delete_account(request):
    user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        user.delete()
        messages.error(request, "account deleted!")
        return redirect('store')
    
    return render(request, 'account/delete-account.html')