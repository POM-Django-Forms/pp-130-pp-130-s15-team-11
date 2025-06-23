from django import forms
from .models import CustomUser

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'first_name', 'last_name', 'middle_name']
        labels = {
            'email': 'Email',
            'password': 'Password',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'middle_name': 'Patronymic',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        self.fields['middle_name'].required = False

class UserLoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')

class UserProfileForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False, label='Password (leave blank to keep unchanged)')
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'middle_name', 'password']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'middle_name': 'Patronymic',
            'password': 'Password',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        self.fields['middle_name'].required = False
        self.fields['password'].required = False