from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import PasswordInput, TextInput

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

    def clean_email(self):
        email = self.cleaned_data.get("email")
        
        # Remove non-breaking spaces and strip whitespace
        email = email.replace('\xa0', '').strip()
        
        # Validate email format
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        
        if len(email) > 254:
            raise forms.ValidationError("This email is too long. Maximum length is 254 characters.")
        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


class UpdateUserForm(forms.ModelForm):
    password = None  # Prevent password from being included in this form

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)  # Correct usage of super
        self.fields['email'].required = True

        def clean_email(self):
            email = self.cleaned_data.get("email")
            
            # Remove non-breaking spaces and strip whitespace
            email = email.replace('\xa0', '').strip()
            
            # Validate email format
            if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("This email is already registered.")
            
            if len(email) > 254:
                raise forms.ValidationError("This email is too long. Maximum length is 254 characters.")
            return email